# Задание No3
# 📌 Создать API для добавления нового пользователя в базу данных.
# Приложение должно иметь возможность принимать POST запросы с данными нового пользователя и сохранять их в базу данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для добавления нового пользователя (метод POST).
# 📌 Реализуйте валидацию данных запроса и ответа.

# Задание No4
# 📌 Создать API для обновления информации о пользователе в базе данных.
# Приложение должно иметь возможность принимать PUT запросы с данными пользователей и обновлять их в базе данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для обновления информации о пользователе (метод PUT).
# 📌 Реализуйте валидацию данных запроса и ответа.

# Задание No5
# 📌 Создать API для удаления информации о пользователе из базы данных.
# Приложение должно иметь возможность принимать DELETE запросы и удалять информацию о пользователе из базы данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для удаления информации о пользователе (метод DELETE).
# 📌 Реализуйте проверку наличия пользователя в списке и удаление его из списка.

# Задание No6
# 📌 Создать веб-страницу для отображения списка пользователей.
# Приложение должно использовать шаблонизатор Jinja для динамического формирования HTML страницы.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен содержать заголовок страницы,
# таблицу со списком пользователей и кнопку для добавления нового пользователя.
# 📌 Создайте маршрут для отображения списка пользователей (метод GET).
# 📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="./ht_05_firstViewOfFastAPI/templates")


users = []


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(UserIn):
    id: int


class UserOut(BaseModel):
    id: int
    name: str
    email: str


for i in range(10):
    users.append(User(
        id=i + 1,
        name=f'n{i + 1}',
        email=f'e{i + 1}@m.t',
        password=f'123{i + 1}'
    ))


@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.post("/users/post/", response_model=UserOut)
async def add_user(new_user: UserIn):
    new_user_id = users[-1].id + 1 if len(users) else 1
    new_user = User(id=new_user_id, name=new_user.name, email=new_user.email, password=new_user.password)
    users.append(new_user)
    return UserOut(id=new_user.id, name=new_user.name, email=new_user.email)


@app.put("/users/put/{user_id}", response_model=UserOut)
async def edit_user(user_id: int, user_in: UserIn):
    for user in users:
        if user.id == user_id:
            user.name = user_in.name
            user.email = user_in.email
            user.password = user_in.password
            return UserOut(id=user.id, name=user.name, email=user.email)
    raise HTTPException(status_code=404, detail='User not found')


@app.delete("/users/delete/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')


@app.get("/new_user/", response_class=HTMLResponse)
async def new_user(request: Request):
    return templates.TemplateResponse('new_user.html', {'request': request})


@app.post("/new_user/", response_class=HTMLResponse)
async def create_user(request: Request,
                      user_name: Annotated[str, Form()],
                      user_email: Annotated[str, Form()],
                      user_password: Annotated[str, Form()]):
    await add_user(UserIn(name=user_name, email=user_email, password=user_password))
    return await get_users(request)


"""через main с использованием jinja2 код почему-то не работает ни с семинарского
занятия, ни в домашнем задании! 
выдает ошибку jinja2.exceptions.templatenotfound: users.html not found
Через uvicorn в терминале - работает! Причина - непонятна"""
if __name__ == "__main__":
    uvicorn.run("ex_03-06:app", host="127.0.0.1", port=8000, reload=True)

# uvicorn ht_05_firstViewOfFastAPI.ex_03-06:app --reload
