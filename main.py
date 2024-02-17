import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from public.users import U_R, database, create_tables

create_tables()

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("Соединение с сервером")
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    print("Соединение разорвано")
    await database.disconnect()

app.include_router(U_R)

@app.get('/', response_class = HTMLResponse)
async def index():
    return "<b> Привет, пользователь! </b>"