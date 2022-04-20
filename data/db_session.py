import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyImageBase = dec.declarative_base()
SqlAlchemyUsersBase = dec.declarative_base()

__factory_user = None
__factory_image = None


def global_init_user_base(db_file):
    global __factory_user

    if __factory_user:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory_user = orm.sessionmaker(bind=engine)

    from . import __all_models_user

    SqlAlchemyUsersBase.metadata.create_all(engine)


def create_session_user_base() -> Session:
    global __factory_user
    return __factory_user()


def global_init_image_base(db_file):
    global __factory_image

    if __factory_image:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory_image = orm.sessionmaker(bind=engine)

    from . import __all_models_image

    SqlAlchemyImageBase.metadata.create_all(engine)


def create_session_image_base() -> Session:
    global __factory_image
    return __factory_image()
