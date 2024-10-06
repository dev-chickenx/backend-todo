from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

DB_DIALECT = "mysql"
DB_DRIVER = "pymysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "db"
DB_PORT = 3306
DB_NAME = "demo"
DB_CHARSET = "utf8"

# URLを作成
DB_URL = URL.create(
    drivername=f"{DB_DIALECT}+{DB_DRIVER}",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={"charset": DB_CHARSET},
)


db_engine = create_engine(DB_URL, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


Base = declarative_base()


def get_db():
    with db_session() as session:
        yield session
