from fastapi import FastAPI as App
from Schemes import User, LoginRequest

app = App()

@app.get("/")
async def read_root():
    return {"Status": "Healthy"}

@app.post("/register")
async def register_user(user: User):
    # Запрос в кафка и базу данных для регистрации пользователя
    return {"Status": "User registered"}

@app.post("/login")
async def login_user(login_request: LoginRequest):
    # Запрос в кафка и базу данных для аутентификации пользователя
    return {"Status": "User logged in"}