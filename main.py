from fastapi import FastAPI as App, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlalchemy import engine, select, update, delete, insert
from Schemas import UserSchema, LoginRequest
from logging import getLogger
from kafkaproducer import produce_message
from db_provider import get_db, User, add_user_to_db, match_user_data, Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from bcrypt import hashpw, gensalt
from settings import settings
from my_token import create_access_token, verify_access_token

logger = getLogger("main")
logger.setLevel("INFO")

security = HTTPBearer()

app = App()

@app.get("/")
async def read_root():
    logger.info("Reading root endpoint")
    return {"Status": "Healthy"}

@app.post("/register")
async def register_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    logger.info("Registering user")
    user.password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

    produce_message("Register request received")
    await add_user_to_db(user, db)
    logger.info(f"User {user.username} registered successfully")
    return {"Status": "User registered"}

@app.post("/login")
async def login_user(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    logger.info("Logging in user")
    produce_message("Login request received")    
    try:
        response: dict = await match_user_data(login_request, db)
        if response["Status"] == "Login failed":
            return response
    except Exception as e:
        raise HTTPException(401, "Неверный логин или пароль")

    logger.info(f"User {login_request.username} logged in successfully")
    access_token = create_access_token(data={"sub": login_request.username})
    return {"Status": "User logged in", "access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)): # type: ignore
    logger.info("Getting current user")
    payload = verify_access_token(credentials.credentials)
    assert payload is not None
    username = payload.get("sub")
    if username is None:
        return {"Status": "No username found in token"}
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        return {"Status": "User not found"}
    return {"username": user.username, "email": user.email, "registered_at": user.registered_at}