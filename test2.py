from requests import get, put, delete, post
import datetime

# Error. Такой работы нет
print(delete("http://127.0.0.1:5000/api/v2/jobs/34534634534").json())

# Error. Такой работы нет
print(get("http://127.0.0.1:5000/api/v2/jobs/34534634534").json())

# Error. Обязательных полей нет
print(put('http://127.0.0.1:8091/api/v2/jobs/', json={
    "work_size": 1
}).json())


# Success. Работа существует
print(get("http://127.0.0.1:5000/api/v2/jobs/1").json())

# Success. Работа существует и удалится
print(delete("http://127.0.0.1:5000/api/v2/jobs/1").json())

# Success. Новая работа успешно добавится
print(put("http://127.0.0.1:5000/api/v2/jobs/", json={
    "team_leader": "1",
    "job": "Cleaning",
    "work_size": 2,
    "collaborators": "2,4,6",
    "start_date": datetime.datetime.now(),
    "end_date": datetime.datetime.now() + datetime.timedelta(days=1),
    "is_finished": False
}).json())
