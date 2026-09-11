from fastapi import FastAPI as App, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlalchemy import engine, select, update, delete, insert
from Schemas import UserSchema, LoginRequest, LoginResponse
from logging import getLogger
from kafkaproducer import produce_message
from db_provider import get_db, User, add_user_to_db
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from bcrypt import hashpw, gensalt
from settings import settings
from my_token import create_access_token, verify_access_token
from bcrypt import checkpw


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

@app.post("/login", response_model=LoginResponse)
async def login_user(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    logger.info("Logging in user")
    produce_message("Login request received")    
    try:
        user = (await db.execute(select(User).where(User.username == login_request.username))).scalar_one_or_none()
        if user is None or not checkpw(login_request.password.encode('utf-8'), user.password.encode('utf-8')): # type: ignore
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        logger.info(f"User {login_request.username}:{user.id} logged in successfully")
        access_token = create_access_token(data={"sub": str(user.id)})
        responce = LoginResponse(
            Status="User logged in",
            access_token=access_token,
            token_type="bearer"
        )
        return responce
    except Exception as e:
        logger.error(f"Error matching user data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)): # type: ignore
    logger.info("Getting current user")
    payload = verify_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Token is invalid")
    id = int(sub)
    if id is None:
        return {"Status": "No username found in token"}
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if user is None:
        return {"Status": "User not found"}
    return {"username": user.username, "email": user.email, "registered_at": user.registered_at}