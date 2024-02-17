# Нужные библиотеки
from fastapi import APIRouter, Body, HTTPException
from models.dbcontext import *
from models.models_user import *
from typing import Annotated, Union
from fastapi.responses import JSONResponse
from starlette import status
from sqlalchemy import select, insert, text, update, create_engine

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from config import settings

from databases import Database

# Данные нужные для подключения к базе данных
DATABASE_URL = settings.POSTGRES_DATABASE_URLS
database = Database(DATABASE_URL)

engine_s = create_engine(DATABASE_URL, echo=True)
# Создание начальной таблицы
def create_tables():
     Base.metadata.drop_all(bind = engine_s)
     Base.metadata.create_all(bind = engine_s)

# Хэширование данных пользователей
secretKey = b'vOVH6sdmpNWjRRIqCc7rdxs01lwHzfr3'

def coder_passwd(cod: str):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(secretKey), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(cod.encode()) + encryptor.finalize()
    return ciphertext.hex()

def decoder_passwd(hash):
    iv = bytes.fromhex(hash["iv"])
    content = bytes.fromhex(hash["content"])
    cipher = Cipher(algorithms.AES(secretKey), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(content) + decryptor.finalize()).decode('utf-8')

U_R = APIRouter(tags = [Tags.users], prefix = '/api/users')

# Получения списка пользователей
@U_R.get("/", response_model = Union[list[Main_User], New_Respons], tags=[Tags.users])
async def get_users_db():
    users = await database.fetch_all(select(User).order_by(User.id.asc()))
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users
# Получение данных пользователя по его id
@U_R.get("/{id}", response_model = Union[Main_User, New_Respons], tags=[Tags.users])
async def get_user(id: int):
    user = await database.fetch_one(select(User).where(User.id == id))
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return user
# Изменение данных пользователя
@U_R.put("/", response_model = Union[Main_User, New_Respons], tags=[Tags.users])
async def edit_person(item: Annotated[Main_User, Body(embed = True, description = "Изменяем данные пользователя через его id")]):
    user = await database.fetch_one(select(User).where(User.id == item.id))
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        user.name = item.name
        user.surname = item.surname
        await database.execute(text(f"update users set name=\'{user.name}\', surname=\'{user.surname}\' where id={item.id};"))
        await database.execute(text("commit;"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в изменении объекта {user}")
    return user
# Добавление нового пользователя
@U_R.post("/", response_model = Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
async def create_user(item: Annotated[Main_User, Body(embed = True, description = "Новый пользователь")]):
    user = User(id = item.id, name = item.name, surname = item.surname, hashed_password = coder_passwd(item.surname))
    if user is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
    try:
        await database.execute(insert(User).values({"id": user.id, "name": user.name, "surname": user.surname, "hashed_password": user.hashed_password}))
        await database.execute(text("commit;"))
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в добавлении объекта {user}")
# Частичное данных пользователя
@U_R.patch("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
async def edit_user(id: int, item: Annotated[Main_User, Body(embed=True, description="Изменяем данные по id")]):   
    user = await database.fetch_one(select(User).where(User.id == id))
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        new_data = item.dict(exclude_unset=True)
        if 'id' in new_data:
            del new_data['id']
        await database.execute(update(User).values(new_data).where(User.id == id))
        await database.execute(text("commit;"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в изменении объекта {user}")
    return user
# Удаление пользователя
@U_R.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
async def delete_person(id: int):
    user = await database.fetch_one(select(User).where(User.id == id))
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        await database.execute(text(f'delete from users where id={id};'))
        await database.execute(text("commit;"))
    except HTTPException:
        JSONResponse(content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Пользователь удалён {id}"})