from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import User
from logging import getLogger
from Schemas import UserSchema, LoginRequest
from settings import settings

logger = getLogger("db_provider")
logger.setLevel("INFO")

async_engine = create_async_engine(
    url = f"{settings.DATABASE_DRIVER}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DATABASE_URL}/{settings.POSTGRES_DB}",
    pool_size=10,
    max_overflow=5,
    pool_timeout=10,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False
)

# Фабрика асинхронных сессий
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Для FastAPI (Dependency Injection)
async def get_db():
    async with async_session() as session:
        yield session

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

async def add_user_to_db(user: UserSchema, db: AsyncSession):
    try:
        await db.execute(insert(User).values(
            username=user.username, 
            email=user.email, 
            password=user.password
        ))
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Возвращаем понятную ошибку клиенту
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    except Exception as e:
        await db.rollback()
        raise e
