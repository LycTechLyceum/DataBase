import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# помолись и уйди, я не знаю что это
# а на самом деле этот файл реализует подключение к файлу sqlite по его относительному пути


SqlAlchemyBase = dec.declarative_base()

__factory = None

''' Создает базу данных при первом вызове по данному адресу,
если она уже была вызвана ранее, то ничего не создает
необходима для инициализации БД через код'''

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip(): # проверяем, что у нас не пустой адрес
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False' # создаем строку подключения к БД
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False) # создаем движок, с которым и будем работать впоследствии
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session: # создаем все объекты, которые еще не были созданы
    global __factory
    return __factory()
