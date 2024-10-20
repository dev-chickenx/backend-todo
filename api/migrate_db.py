from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from api.models.task import Base

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

engine = create_engine(DB_URL, echo=True)


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
