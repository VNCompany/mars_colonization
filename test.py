from requests import get, put, delete, post

# Error. Такого пользователя по идее нет в базе
print(delete("http://127.0.0.1:5000/api/v2/users/34534634534").json())

# Error. Такого пользователя по идее нет в базе
print(get("http://127.0.0.1:5000/api/v2/users/34534634534").json())

# Error. Обязательных полей нет
print(put('http://127.0.0.1:8091/api/v2/users/', json={
    "surname": 0
}).json())


# Success. Пользователь существует
print(get("http://127.0.0.1:5000/api/v2/users/1").json())

# Success. Пользователь существует и удалится
print(delete("http://127.0.0.1:5000/api/v2/users/1").json())

# Success. Новый пользователь успешно добавится
print(put("http://127.0.0.1:5000/api/v2/users/", json={
    "surname": "Ivanov",
    "name": "Ivan",
    "age": 32,
    "position": "master",
    "speciality": "engineer",
    "address": "module_3",
    "email": "i.vanov123@yandex.ru"
}).json())
