from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_DIALECT = "mysql"
DB_DRIVER = "aiomysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "db"
DB_PORT = 3306
DB_NAME = "demo"
DB_CHARSET = "utf8"

# URLを作成
ASYNC_DB_URL = URL.create(
    drivername=f"{DB_DIALECT}+{DB_DRIVER}",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={"charset": DB_CHARSET},
)


async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
