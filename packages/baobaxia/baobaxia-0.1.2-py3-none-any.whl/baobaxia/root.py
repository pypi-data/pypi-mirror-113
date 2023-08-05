from pathlib import Path
from datetime import date, datetime
import os
from collections.abc import MutableMapping

from typing import Optional, List
from pydantic import BaseModel
from configparser import ConfigParser 

from .sankofa import Sankofa
from .util import str_to_hash
from .saberes import (
    Saber,
    Balaio,
    Mucua,
    Mocambola,
    Mocambo,
    SaberesConfig,
    SaberesDataStore
)

class BaobaxiaError(RuntimeError):
    pass

class Session():

    timeout = 900 # 15 minutos

    def __init__(self, mocambola: Mocambola):
        super().__init__()
        self.mocambola = mocambola
        self.started = datetime.now()
        self.alive_at = datetime.now()
        self.token = str_to_hash(
            mocambola.username +
            str(round(self.started.microsecond * 1000)))

    def is_alive(self, safe = True):
        result = True
        if self.alive_at is None:
            result = False
        else:
            delta = datetime.now() - self.alive_at
            result = self.__class__.timeout > delta.seconds
        if not result and not safe:
            raise BaobaxiaError('Sessão expirou')
        return result

    def keep_alive(self):
        self.is_alive(False)
        self.alive_at = datetime.now()
        return self

    def close(self):
        self.alive_at = None

class SessionDict(MutableMapping):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._by_token = {}
        self._by_mocambola = {}
        self.update(dict(*args, **kwargs))

    def __contains__(self, key):
        if isinstance(key, Mocambola):
            return key.username in self._by_mocambola
        return key in self._by_token

    def __getitem__(self, key):
        if isinstance(key, Mocambola):
            if key.username in self._by_mocambola and \
                    self._by_mocambola[key.username].is_alive():
                return self._by_mocambola[key.username].keep_alive()
            session = Session(key.copy(exclude={'password_hash', 'recovery_answer_hash'}))
            self[key] = session
            return session
        else:
            return self._by_token[key].keep_alive()

    def __setitem__(self, key, value):
        if not isinstance(value, Session):
            raise BaobaxiaError("Sessão inválida")
        value.is_alive(False)
        if isinstance(key, Mocambola) and value.mocambola.username != key.username:
            raise BaobaxiaError("Mocambola inválido")
        if isinstance(key, str) and value.token != key:
            raise BaobaxiaError("Token inválido")
        self._by_mocambola[value.mocambola.username] = value
        self._by_token[value.token] = value

    def __delitem__(self, key):
        session = self[key]
        session.close()
        del self._by_mocambola[session.mocambola.username]
        del self._by_token[session.token]

    def __iter__(self):
        return iter(self._by_token)

    def __len__(self):
        return len(self._by_token)


class Baobaxia():

    _MOCAMBOLA = Mocambola(username='exu', email='exu@mocambos.net')

    def __init__(self, config: Optional[SaberesConfig] = None):
        if config == None:
            config_file = ConfigParser()
            config_file.read(os.path.join(os.path.expanduser("~"), '.baobaxia.conf'))
            config = SaberesConfig.parse_obj(config_file['default'])
            '''
            config = SaberesConfig(
                data_path = Path(config_file['default']['data_path']),
                saber_file_ext = config_file['default']['saber_file_ext'],
                balaio_local = config_file['default']['balaio_local'],
                mucua_local = config_file['default']['mucua_local'],
                smid_len = config_file['default'].getint('smid_len'),
                slug_smid_len = config_file['default'].getint('slug_smid_len'),
                slug_name_len = config_file['default'].getint('slug_name_len'),
                slug_sep = config_file['default']['slug_sep']
                )
            '''
        self.config = config
        self.datastore = SaberesDataStore(self.config)
        self.reload_balaios()
        self._sessions = SessionDict()

    def reload_balaios(self):
        balaios_list = self.datastore.create_dataset(
            model=Balaio).collect_saberes('*/')
        self._balaios = {}
        self._mocambolas = {}
        self._mucuas_por_balaio = {}
        self._mocambolas_por_mucua = {}
        for balaio in balaios_list:
            self._balaios[balaio.slug] = balaio
            self._mucuas_por_balaio[balaio.slug] = {}
            self._mocambolas_por_mucua[balaio.slug] = {}
            mucuas = self.datastore.create_dataset(
                model=Mucua, balaio=balaio.slug).collect_saberes('*/')
            for mucua in mucuas:
                self._mucuas_por_balaio[balaio.slug][mucua.slug] = mucua
                self._mocambolas_por_mucua[balaio.slug][mucua.slug] = {}
                mocambolas = self.datastore.create_dataset(
                    model=Mocambola, balaio=balaio.slug,
                    mucua=mucua.slug).collect_saberes('mocambolas/*/')
                for mocambola in mocambolas:
                    self._mocambolas_por_mucua[balaio.slug][mucua.slug][
                        mocambola.data.username] = mocambola

        self._balaio_local = self._balaios[
            self.config.balaio_local]
        self._mucua_local = self._mucuas_por_balaio[
            self.config.balaio_local][self.config.mucua_local]

    def list_balaios(self, token: str):
        session = self._sessions[token]
        result = []
        for key, value in self._balaios.items():
            result.append(value.copy())
        return result

    def get_balaio(self, slug: str, token: str):
        session = self._sessions[token]
        return self._balaios[slug].copy()

    def put_balaio(self, *,
                    slug: Optional[str] = None,
                    name: str,
                    token: str):
        session = self._sessions[token]
        dataset = self.datastore.create_dataset(
            mocambola=session.mocambola,
            model=Balaio)
        if slug is None:
            balaio = dataset.settle_saber(
                path = Path('.'),
                name = name,
                data = Balaio(),
                slug_dir = True
            )
            self._balaios[balaio.slug] = balaio
            self._mucuas_por_balaio[balaio.slug] = {}
            self._mocambolas_por_mucua[balaio.slug] = {}
        else:
            balaio = self._balaios[slug]
            balaio.name = name
            saber = dataset.settle_saber(
                path=balaio.path, name=name, data=balaio.data)
            
        Sankofa.create_balaio(balaio=balaio.name, description=balaio.name,
                              config=self.config)
        return balaio.copy()

    def del_balaio(self,
                   slug: str,
                   token: str):
        session = self._sessions[token]
        if slug == self._balaio_local.slug:
            # Baobaxia não pode deixar para trás o balaio de seus próprios saberes.
            raise RuntimeError('Cannot delete balaio local.')
        dataset = self.datastore.create_dataset(
            mocambola = session.mocambola,
            model = Balaio
        )
        
        Sankofa.remove(saberes=[self._balaios[slug],],
                       mocambola=session.mocambola,
                       config=self.config)
        dataset.drop_saber(Path(slug))

        del self._balaios[slug]
        del self._mucuas_por_balaio[slug]
        del self._mocambolas_por_mucua[slug]


    def list_mucuas(self,
                    balaio_slug: str,
                    token: str):
        session = self._sessions[token]
        result = []
        for key, value in self._mucuas_por_balaio[balaio_slug].items():
            result.append(value.copy())
        return result

    def get_mucua(self,
                  balaio_slug: str,
                  mucua_slug: str,
                  token: str):
        session = self._sessions[token]
        return self._mucuas_por_balaio[balaio_slug][mucua_slug].copy()

    def put_mucua(self, *,
                  balaio_slug: str,
                  name: str,
                  mucua_slug: Optional[str] = None,
                  token: str):
        session = self._sessions[token]
        dataset = self.datastore.create_dataset(
            mocambola=session.mocambola,
            model=Mucua,
            balaio=balaio_slug
        )
        if mucua_slug is None:
            mucua = dataset.settle_saber(
                path=Path('.'),
                name=name,
                data=Mucua(),
                slug_dir=True
            )
            self._mucuas_por_balaio[balaio_slug][mucua.slug] = mucua
            self._mocambolas_por_mucua[balaio_slug][mucua.slug] = {}
        else:
            mucua = self._mucuas_por_balaio[balaio_slug][mucua_slug]
            mucua.name = name
            dataset.settle_saber(
                path=mucua.path, name=name, data=mucua.data)

        Sankofa.add(saberes=[mucua], mocambola=session.mocambola,
                    config=self.config)
        
        return mucua.copy()

    def del_mucua(self,
                  balaio_slug: str,
                  mucua_slug: str,
                  token: str):
        session = self._sessions[token]
        if balaio_slug == self._balaio_local.slug and \
           mucua_slug == self._mucua_local.slug:
            # Baobaxia não pode deixar para trás a mucua de seus próprios saberes.
            raise RuntimeError('Cannot delete mucua local.')
            
        dataset = self.datastore.create_dataset(
            mocambola=session.mocambola,
            model=Mucua,
            balaio=balaio_slug
        )
        
        Sankofa.remove(saberes=[self._mucuas_por_balaio[balaio_slug][mucua_slug],],
                       mocambola=session.mocambola,
                       config=self.config)

        del self._mucuas_por_balaio[balaio_slug][mucua_slug]
        del self._mocambolas_por_mucua[balaio_slug][mucua_slug]

        #dataset.drop_saber(Path(mucua_slug))

    def list_mocambos(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      token: str):
        session = self._sessions[token]
        result = []
        for mocambo in self._mocambos_por_mucua[
                balaio_slug][mucua_slug]:
            result.append(mocambo.copy(exclude={'mocambolas'}))
        return result

    def get_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo_slug: str,
                    token: str):
        session = self._sessions[token]
        return self._mocambos_por_mucua[balaio_slug][mucua_slug][
            mocambo_slug].copy(exclude={'mocambolas'})
    def put_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo: Saber,
                    token: str):
        raise NotImplementedError()
    def del_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo_slug: str,
                    token, str):
        raise NotImplementedError()

    def list_mocambolas(self, *,
                        balaio_slug: str,
                        mucua_slug: str,
                        token: str):
        session = self._sessions[token]
        result = []
        for mocambola in self._mocambolas_por_mucua[balaio_slug][mucua_slug].values():
            print("***" + str(mocambola))
            result.append(mocambola.data.copy(exclude={
                'password_hash', 'recovery_answer_hash'}))
        return result

    def get_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      username: str,
                      token: str):
        session = self._sessions[token]
        return self._mocambolas_por_mucua[balaio_slug][mucua_slug][
                username].data.copy(exclude={'password_hash', 'recovery_answer_hash'})

    def put_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      username: str,
                      mocambola: Mocambola,
                      password: Optional[str] = None,
                      recovery_answer: Optional[str] = None,
                      token: str):
        session = self._sessions[token]
        dataset = self.datastore.create_dataset(
            mocambola=session.mocambola,
            model=Mocambola,
            balaio=balaio_slug,
            mucua=mucua_slug)

        if username in self._mocambolas_por_mucua[balaio_slug][mucua_slug]:
            print(username)
            if password is not None:
                raise BaobaxiaError('Para mudar a senha use set_password')
            mocambola_saber = self._mocambolas_por_mucua[balaio_slug][mucua_slug][username]
            mocambola_old = mocambola_saber.data
            mocambola_new = mocambola.copy()
            mocambola_new.password_hash = mocambola_old.password_hash
            if recovery_answer is not None:
                mocambola_new.recovery_answer_hash = str_to_hash(recovery_answer)
            else:
                mocambola_new.recovery_answer_hash = mocambola_old.recovery_answer_hash
            mocambola_saber = dataset.settle_saber(
                    path=mocambola_saber.path,
                    name=mocambola.username,
                    data=mocambola_new)
        else:
            mocambola.password_hash = str_to_hash(password)
            mocambola.recovery_answer_hash = str_to_hash(recovery_answer)
            mocambola_saber = dataset.settle_saber(
                    path=Path('mocambolas'),
                    name=mocambola.username,
                    data=mocambola.copy(),
                    slug_dir=True)
            self._mocambolas_por_mucua[balaio_slug][mucua_slug][username] = mocambola_saber

        Sankofa.add(saberes=[mocambola_saber], mocambola=session.mocambola,
                    config=self.config)
        
        return mocambola_saber.data.copy(exclude={'password_hash', 'recovery_answer_hash'})
        

    def del_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      username: str,
                      token: str):
        session = self._sessions[token]
        mocambola_saber = self._mocambolas_por_mucua[balaio_slug][mucua_slug][username]
        dataset = self.datastore.create_dataset(
            mocambola=session.mocambola,
            model=Mocambola,
            balaio=balaio_slug,
            mucua=mucua_slug).drop_saber(mocambola_saber.path)
        del self._mocambolas_por_mucua[balaio_slug][mucua_slug][username]

        Sankofa.remove(saberes=[dataset,], mocambola=session.mocambola,
                       config=self.config)

    def discover_saberes(self, *,
                         balaio_slug: str,
                         mucua_slug: str,
                         model: type,
                         patterns: List[str],
                         field_name: Optional[str] = None,
                         list_field_name: Optional[str] = None,
                         index_function: Optional[callable] = None
    ):
        if field_name is None:
            field_name = model.__name__.lower()
        if list_field_name is None:
            list_field_name = field_name + 's'

        if not hasattr(self, 'saberes'):
            self.saberes = {}
        if balaio_slug not in self.saberes:
            self.saberes[balaio_slug] = {}
        if mucua_slug not in self.saberes[balaio_slug]:
            self.saberes[balaio_slug][mucua_slug] = {}
        self.saberes[balaio_slug][mucua_slug][field_name] = {}

        dataset = self.datastore.create_dataset(
            balaio = balaio_slug,
            mucua = mucua_slug,
            model = model)

        for pattern in patterns:
            saberes = dataset.collect_saberes(pattern)
            for saber in saberes:
                self.saberes[balaio_slug][mucua_slug][
                    field_name][saber.path] = saber
                if index_function is not None:
                    index_function(saber)

        def list_method_template(token: Optional[str] = None):
            result = []
            for key, saber in self.saberes[balaio_slug][mucua_slug][
                    field_name].items():
                result.append(saber)
            return result
        setattr(self, 'list_'+list_field_name, list_method_template)
        
        def find_method_template(
                filter_function: Optional[callable] = None,
                sorted_function: Optional[callable] = None,
                sorted_reverse: bool = False,
                token: Optional[str] = None):
            result = []
            for key, saber in self.saberes[balaio_slug][mucua_slug][
                    field_name].items():
                if filter_function is None or filter_function(saber):
                    result.append(saber)
            if sorted_function is not None:
                result = sorted(result, key = sorted_function, reverse = sorted_reverse)
            return result
        setattr(self, 'find_'+list_field_name, find_method_template)

        def get_method_template(path: Path, token: str):
            session = self._sessions[token]
            return self.saberes[balaio_slug][mucua_slug][
                field_name][path]
        setattr(self, 'get_'+field_name, get_method_template)

        def put_method_template(*, path: Path,
                                name: Optional[str] = None,
                                data: Optional[BaseModel] = None,
                                token: str,
                                slug_dir: bool = False):
            session = self._sessions[token]
            saber = self.datastore.create_dataset(
                    balaio = balaio_slug,
                    mucua = mucua_slug,
                    model = model,
                    mocambola = session.mocambola).settle_saber(
                        path = path, name = name,
                        data = data, slug_dir = slug_dir)
            path = path / saber.slug if slug_dir else path
            self.saberes[balaio_slug][mucua_slug][
                field_name][path] = saber

            Sankofa.add(saberes=[saber], mocambola=session.mocambola,
                        config=self.config)

            return self.saberes[balaio_slug][mucua_slug][
                field_name][path]
        setattr(self, 'put_'+field_name, put_method_template)

        def del_method_template(path: Path, token: str):
            session = self._sessions[token]
            dataset = self.datastore.create_dataset(
                balaio = balaio_slug,
                mucua = mucua_slug,
                model = model,
                mocambola = session.mocambola)
            Sankofa.remove(saberes=[self.saberes[balaio_slug][mucua_slug][
                field_name][path]], mocambola=session.mocambola,
                           config=self.config)
            del self.saberes[balaio_slug][mucua_slug][
                 field_name][path]
            dataset.drop_saber(path)
        setattr(self, 'del_'+field_name, del_method_template)
        
    def _put_mocambola_saber(self, *,
                    username: str,
                    balaio_slug: Optional[str] = None,
                    mucua_slug: Optional[str] = None,
                    mocambola: Saber):
        balaio_slug = self._balaio_local.slug if balaio_slug is None else balaio_slug
        mucua_slug = self._mucua_local.slug if mucua_slug is None else mucua_slug
        self._mocambolas_por_mucua[balaio_slug][mucua_slug][username] = mocambola

    def _find_mocambola_saber(self, *,
                    username: str,
                    balaio_slug: Optional[str] = None,
                    mucua_slug: Optional[str] = None):
        balaio_slug = self._balaio_local.slug if balaio_slug is None else balaio_slug
        mucua_slug = self._mucua_local.slug if mucua_slug is None else mucua_slug
        if username not in self._mocambolas_por_mucua[
                balaio_slug][mucua_slug]:
            raise BaobaxiaError('Mocambola não encontrado')
        return  self._mocambolas_por_mucua[balaio_slug][mucua_slug][username]

    def _check_hash(self, *,
                    username: str,
                    password: Optional[str] = None,
                    recovery_answer: Optional[str] = None,
                    balaio_slug: Optional[str] = None,
                    mucua_slug: Optional[str] = None):
        saber = self._find_mocambola_saber(username=username,
                                           balaio_slug=balaio_slug,
                                           mucua_slug=mucua_slug)
        str_to_check = None
        hash_to_check = None
        if password is not None:
            str_to_check = password
            hash_to_check = saber.data.password_hash
        elif recovery_answer is not None:
            str_to_check = recovery_answer
            hash_to_check = saber.data.recovery_answer_hash
        else:
            raise BaobaxiaError('Erro de autenticação')

        if str_to_hash(str_to_check) != hash_to_check:
            raise BaobaxiaError('Erro de autenticação')

        return saber

    def authenticate(self, *,
                    username: str,
                    password: Optional[str] = None,
                    recovery_answer: Optional[str] = None,
                    balaio_slug: Optional[str] = None,
                    mucua_slug: Optional[str] = None):
        saber = self._check_hash(
            username = username,
            password = password,
            recovery_answer = recovery_answer,
            balaio_slug = balaio_slug,
            mucua_slug = mucua_slug
        )
        return self._sessions[saber.data].token

    def set_password(
            self, *,
            new_password: str,
            password: Optional[str] = None,
            recovery_answer: Optional[str] = None,
            token: str):
        session = self._sessions[token].keep_alive()
        mocambola = session.mocambola
        saber = self._check_hash(
            username = mocambola.username,
            password = password,
            recovery_answer = recovery_answer
        )
        mocambola.password_hash = str_to_hash(new_password)
        dataset = self.datastore.create_dataset(
            mocambola=mocambola,
            model=Mocambola,
            balaio=self._balaio_local.slug,
            mucua=self._mucua_local.slug)
        saber = dataset.settle_saber(
            path=saber.path,
            name=mocambola.username,
            data=mocambola)
        self._put_mocambola_saber(username=mocambola.username, mocambola=saber)

