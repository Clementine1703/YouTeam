from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


db_username = "user"
db_password = "password123"
db_url = "127.0.0.1:3306"
db_name = "main"

DATABASE_URL = f'postgresql+asyncpg://{db_username}:{db_password}@{db_url}/{db_name}'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)