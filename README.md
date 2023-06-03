# sql-trainig
Утилита представляет из себя приложения с графическим интерфейсом, 
позволяющее работать с базой данных без написания запросов.
В модуле, отвечающем за обращение к БД, реализованы основные CRUD операции.
Валидация даных происходит как на уровне прослойки к БД, так и в самой базе данных,
за исключением некоторых моментов, которые неудобно реализовывать в SQLite
(например, валидация номера телефона).
## Установка
### MS Windows
```
python -m venv <venv_name>
.\<venv_name>\Scripts\Activate.ps1
pip install -r requirements.txt
```
### Linux
```
python3 -m venv <venv_name>
source <venv_name>/bin/activate
pip install -r requirements.txt
```

## Использование
```
python3 main.py
```

## Схема БД
![Pucture of db schema](https://github.com/rnjghjxbnfknjnkfgjxrf/sql-training/blob/main/db_schema.png?raw=True)
