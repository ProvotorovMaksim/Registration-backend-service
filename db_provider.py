from sqlalchemy import Column, Integer, String, ForeignKey, insert, update, delete, select
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime
from logging import getLogger
from Schemas import UserSchema, LoginRequest
from settings import settings
from bcrypt import checkpw

logger = getLogger("db_provider")
logger.setLevel("INFO")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    registered_at = Column(String, default=datetime.now().isoformat())

sqlalchemy_url = settings.DATABASE_URL

engine = create_async_engine(sqlalchemy_url, echo=True, future=True)

async def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

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


async def match_user_data(login_request: LoginRequest, db: AsyncSession) -> dict:
    try:
        result = await db.execute(select(User).where(User.username == login_request.username))
        user = result.scalar_one_or_none()
        if user is None or not checkpw(login_request.password.encode('utf-8'), user.password.encode('utf-8')): # type: ignore
            logger.warning(f"Login failed for user: {login_request.username}, {login_request.password} {user.password}") #type: ignore
            print(f"Login failed for user: {login_request.username}, {login_request.password} {user.password}") #type: ignore
            return {"Status": "Login failed"}
        return {"Status": "Login successful"}
    except Exception as e:
        logger.error(f"Error matching user data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
