from sqlalchemy import text

from src.config.database import async_session


async def check_db_connection():
    async with async_session() as session:
        try:
            result = await session.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("Database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")