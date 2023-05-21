import re
import sqlite3
from app.query_utils import INIT_DB_QUERY
from typing import Literal, Union
from datetime import datetime


class DB:
    def __init__(self):
        self._connection = sqlite3.connect('app.db')
        self._cursor = self._connection.cursor()
        self._cursor.executescript(INIT_DB_QUERY)
        self._connection.commit()

    def close_connection(self) -> None:
        self._cursor.close()
        self._connection.close()

    def _execute(self, query: str, *args) -> list:
        try:
            res = self._cursor.execute(query, args)
            self._connection.commit()
        except Exception as err:
            raise DBExecuteQueryError(str(err))
        else:
            return res.fetchall()

    @staticmethod
    def validate_name(name: str) -> bool:
        return re.match('^([а-я]+)$', name) is not None

    @staticmethod
    def validate_race_name(race_name: str) -> bool:
        return re.match('^([а-я][a-я ]*)$', race_name) is not None

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        return re.match(
            '(\+7|8)[ -]?[0-9]{3}[ -]?[0-9]{3}[ -]?([0-9]{2}[ -]?[0-9]{2}|[0-9]{4})',
            phone_number) is not None

    @staticmethod
    def validate_date(date: str) -> bool:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def create_hippodrome(self, name: str):
        name = name.strip().lower()

        if re.search('[0-9]', name) is not None:
            raise HippodromeNameError()

        self._execute("""
            INSERT INTO "Hippodrome" (name)
            VALUES (?);
        """, name.capitalize())

    def create_owner(self, name: str, telephone: str, address: str):
        name = name.strip().lower()
        telephone.strip()

        if not DB.validate_name(name):
            raise NameError()
        elif not DB.validate_phone_number(telephone):
            raise PhoneNumberError()

        self._execute("""
            INSERT INTO "Owner" (name, telephone, address)
            VALUES (?, ?, ?);
        """, name.capitalize(), telephone, address)

    def create_horse(self,
                     name: str,
                     age: int,
                     gender: Union[Literal['мужской'], Literal['женский']],
                     owner_id: int):
        name = name.strip().lower()
        gender = gender.strip().lower()
        try:
            age = int(age)
        except TypeError:
            raise AgeError()

        if not DB.validate_name(name):
            raise NameError()
        elif age < 0:
            raise AgeError()
        elif gender not in ('мужской', 'женский'):
            raise GenderError()

        self._execute("""
            INSERT INTO "Horse" (name, age, gender, owner_id)
            VALUES (?, ?, ?, ?);
        """, name.capitalize(), age, gender, owner_id)

    def create_jockey(self,
                     name: str,
                     age: int,
                     address: str,
                     rating: int):
        name = name.strip().lower()
        address = address.strip()
        try:
            age = int(age)
        except TypeError:
            raise JockeyAgeError()

        if not DB.validate_name(name):
            raise NameError()
        elif age < 18:
            raise JockeyAgeError()

        self._execute("""
            INSERT INTO "Jockey" (name, age, address, rating)
            VALUES (?, ?, ?, ?);
        """, name.capitalize(), age, address, rating)

    def create_race(self,
                    name: str,
                    date: str,
                    hippodrome_id: int):
        name = name.strip()
        date = date.strip()

        if not DB.validate_race_name(name):
            raise NameError()
        elif not DB.validate_date(date):
            raise DateError()

        self._execute("""
            INSERT INTO "Race" (name, date, hippodrome_id)
            VALUES (?, date(?), ?);
        """, name, date, hippodrome_id)
        return self._cursor.lastrowid

    def create_race_result(self,
                           result_place: int,
                           result_time: int,
                           race_id: int,
                           horse_id: int,
                           jockey_id: int):
        try:
            result_place = int(result_place)
            result_time = int(result_time)
            if result_time <= 0 or result_place <= 0:
                raise ValueError()
        except ValueError:
            raise ResultAndPlaceError()

        self._execute("""
            INSERT INTO "Race_result" (result_place, result_time, race_id, horse_id, jockey_id)
            VALUES (?, ?, ?, ?, ?);
        """, result_place, result_time, race_id, horse_id, jockey_id)        


    def get_all_horses(self) -> list[tuple]:
        return self._execute("""
            SELECT
                h.id, h.name, h.age, h.gender, o.name, o.id
            FROM
                "Horse" as h
            JOIN
                "Owner" as o
            ON
                h.owner_id = o.id;
        """)

    def get_all_owners(self) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Owner";
        """)

    def get_all_jockeys(self) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Jockey";
        """)

    def get_all_races(self) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Race";
        """)

    def get_all_hippodromes(self) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Hippodrome";
        """)

    def get_jockeys_that_not_in_race(self, race_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Jockey"
            WHERE
                id NOT IN (
                    SELECT
                        jockey_id
                    FROM
                        "Race_result"
                    WHERE
                        race_id = ?
                );
        """, race_id)

    def get_horses_that_not_in_race(self, race_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Horse"
            WHERE
                id NOT IN (
                    SELECT
                        horse_id
                    FROM
                        "Race_result"
                    WHERE
                        race_id = ?
                );
        """, race_id)

    def get_owner(self, owner_id) -> list[tuple]:
        return self._execute("""
            SELECT
                name, address, telephone
            FROM
                "Owner";
        """)

    def get_owner_horses(self, owner_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Horse"
            WHERE
                owner_id = ?;
        """, owner_id)

    def get_horse(self, horse_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                h.name, h.age, h.gender, o.name, o.id
            FROM
                "Horse" as h
            JOIN
                "Owner" as o
            ON
                h.owner_id = o.id
            WHERE
                h.id = ?;
        """, horse_id)

    def get_races_with_horse(self, horse_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                r.id, r.name
            FROM
                "Race" as r
            JOIN
                "Race_result" as rr
            ON
                rr.race_id = r.id
            WHERE
                rr.horse_id = ?;
        """, horse_id)

    def get_race(self, race_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                r.name, r.date, h.name, h.id
            FROM
                "Race" as r
            JOIN
                "Hippodrome" as h
            ON
                r.hippodrome_id = h.id
            WHERE
                r.id = ?;
        """, race_id)

    def get_race_results(self, race_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                rr.id, j.name, h.name, rr.result_place, rr.result_time,
                j.id, h.id
            FROM
                "Race_result" as rr
            JOIN
                "Jockey" as j
            ON
                j.id = rr.jockey_id
            JOIN
                "Horse" as h
            ON
                h.id = rr.horse_id
            WHERE
                rr.race_id = ?;
        """, race_id)

    def get_jockey(self, jockey_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                name, age, address, rating
            FROM
                "Jockey"
            WHERE
                id = ?;
        """, jockey_id)

    def get_jockeys_races(self, jockey_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                r.id, r.name
            FROM
                "Race_result" as rr
            JOIN
                "Race" as r
            ON
                rr.race_id = r.id
            WHERE
                rr.jockey_id = ?;
        """, jockey_id)

    def get_hippodrome_races(self, hippodrome_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                id, name
            FROM
                "Race"
            WHERE
                hippodrome_id = ?;
        """, hippodrome_id)

    def get_hippodrome(self, hippodrome_id: int) -> list[tuple]:
        return self._execute("""
            SELECT
                name
            FROM
                Hippodrome
            WHERE
                id = ?;
        """, hippodrome_id)

    def delete_owner(self, owner_id: int):
        self._execute("""
            DELETE FROM "Owner"
            WHERE id = ?;
        """, owner_id)

    def delete_horse(self, horse_id: int):
        self._execute("""
            DELETE FROM "Horse"
            WHERE id = ?;
        """, horse_id)

    def delete_jockey(self, jokey_id: int):
        self._execute("""
            DELETE FROM "Jockey"
            WHERE id = ?;
        """, jokey_id)

    def delete_race(self, race_id: int):
        self._execute("""
            DELETE FROM "Race"
            WHERE id = ?;
        """, race_id)

    def delete_race_result(self, race_result_id: int):
        self._execute("""
            DELETE FROM "Race_result"
            WHERE id = ?;
        """, race_result_id)

    def delete_hippodrome(self, hippodrome_id: int):
        self._execute("""
            DELETE FROM "Hippodrome"
            WHERE id = ?;
        """, hippodrome_id)

class DBExecuteQueryError(Exception):
    def __init__(self, err_message: str) -> None:
        super().__init__('Ошибка при выполнении запроса к БД:\n'+err_message)

class PhoneNumberError(Exception):
    def __init__(self) -> None:
        super().__init__('Неправильный формат номера телефона:\n' +
                         'Номер должен состоять из 11 цифр, начинаться с 8 или с +7, ' +
                         'в качестве разделителей можно использовать пробел или знак тире.')

class GenderError(Exception):
    def __init__(self) -> None:
        super().__init__('Неправильный пол:\n'+
                         'должен быть: мужской/женский')

class NameError(Exception):
    def __init__(self, err_message: str = None) -> None:
        if err_message is None:
            err_message = 'Имя должно состоять только из букв русского алфавита.'
        super().__init__('Неправильный формат имени:\n'+err_message)

class HippodromeNameError(NameError):
    def __init__(self) -> None:
        super().__init__('Название ипподрома не должно содержать числа.')

class AgeError(Exception):
    def __init__(self, err_message: str = None) -> None:
        if err_message is None:
            err_message = 'Возраст должен быть представлен как целое неотрицательное число.'
        super().__init__('Неправильный формат возраста:\n'+err_message)

class JockeyAgeError(AgeError):
    def __init__(self) -> None:
        super().__init__('Возраст жокея должен быть представлен как целое число не меньшее 18.')

class DateError(Exception):
    def __init__(self) -> None:
        super().__init__('Неправильный формат даты:\nДолжен быть YYYY-MM-DD.')

class ResultAndPlaceError(Exception):
    def __init__(self) -> None:
        super().__init__('Занятое место и время прибытия к финишу должны быть целыми положительными числами.')