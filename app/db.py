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
        self._cursor.execute('PRAGMA foreign_keys = ON;')
        self._connection.commit()
        print('Connection created')

    def close_connection(self) -> None:
        self._cursor.close()
        self._connection.close()
        print('Connection closed')

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
            '^(\+7|8)[ -]?[0-9]{3}[ -]?[0-9]{3}[ -]?([0-9]{2}[ -]?[0-9]{2}|[0-9]{4})$',
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
            raise HippodromeNameError('incorrect_name')
        name = name.capitalize()
        if any(name in x for x in self._execute('SELECT name FROM "Hippodrome";')):
            raise HippodromeNameError('name_not_unique')

        self._execute("""
            INSERT INTO "Hippodrome" (name)
            VALUES (?);
        """, name)

        return self._cursor.lastrowid

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

        return self._cursor.lastrowid

    def create_horse(self,
                     name: str,
                     age: int,
                     gender: Union[Literal['мужской'], Literal['женский']],
                     owner_id: int):
        if not isinstance(owner_id, int):
            raise IDError()

        name = name.strip().lower()
        gender = gender.strip().lower()
        try:
            age = int(age)
        except ValueError:
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

        return self._cursor.lastrowid

    def create_jockey(self,
                     name: str,
                     age: str,
                     address: str,
                     rating: str):
        name = name.strip().lower()
        address = address.strip()
        try:
            age = int(age)
        except ValueError:
            raise JockeyAgeError()

        try:
            rating = int(rating)
        except ValueError:
            raise JockeyRatingError()

        if not DB.validate_name(name):
            raise NameError()
        elif age < 18:
            raise JockeyAgeError()

        self._execute("""
            INSERT INTO "Jockey" (name, age, address, rating)
            VALUES (?, ?, ?, ?);
        """, name.capitalize(), age, address, rating)

        return self._cursor.lastrowid

    def create_race(self,
                    name: str,
                    date: str,
                    hippodrome_id: int):
        if not isinstance(hippodrome_id, int):
            raise IDError()

        name = name.strip().lower()
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
                           result_place: str,
                           result_time: str,
                           race_id: int,
                           horse_id: int,
                           jockey_id: int):
        if not isinstance(race_id, int)\
           or not isinstance(jockey_id, int)\
           or not isinstance(horse_id, int):
            raise IDError()

        try:
            result_time = int(result_time)
            if result_time <= 0:
                raise ValueError()
        except ValueError:
            raise RaceResultTimeError()

        try:
            result_place = int(result_place)
            if result_place < 1 or result_place > 20:
                raise ValueError()
        except ValueError:
            raise RaceResultPlaceError()

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
        if not isinstance(race_id, int):
            raise IDError()

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
        if not isinstance(race_id, int):
            raise IDError()

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
        if not isinstance(owner_id, int):
            raise IDError()

        return self._execute("""
            SELECT
                name, address, telephone
            FROM
                "Owner"
            WHERE
                id = ?;
        """, owner_id)

    def get_owner_horses(self, owner_id: int) -> list[tuple]:
        if not isinstance(owner_id, int):
            raise IDError()

        return self._execute("""
            SELECT
                id, name
            FROM
                "Horse"
            WHERE
                owner_id = ?;
        """, owner_id)

    def get_owners_with_horses_count_in_range(self,
                                               horses_from: str,
                                               horses_to: str) -> list[tuple]:
        if not horses_from:
            horses_from = self._execute("""
                SELECT
                    COUNT(h.id) as hc
                FROM
                    "Owner" as o
                LEFT OUTER JOIN
                    "Horse" as h
                ON
                    h.owner_id = o.id
                GROUP BY o.id
                ORDER BY hc ASC
                LIMIT 1;
            """)[0][0]

        if not horses_to:
            horses_to = self._execute("""
                SELECT
                    COUNT(h.id) as hc
                FROM
                    "Owner" as o
                LEFT OUTER JOIN
                    "Horse" as h
                ON
                    h.owner_id = o.id
                GROUP BY o.id
                ORDER BY hc DESC
                LIMIT 1;
            """)[0][0]

        try:
            horses_from = int(horses_from)
            horses_to = int(horses_to)
        except ValueError:
            raise CountValueError('Количество лошадей')

        return self._execute("""
            SELECT
                o.id, o.name, COUNT(h.id) as hc
            FROM
                "Owner" as o
            LEFT OUTER JOIN
                "Horse" as h
            ON
                h.owner_id = o.id
            GROUP BY o.id
            HAVING hc BETWEEN ? and ?
            ORDER BY hc ASC;
        """, horses_from, horses_to)

    def get_horse(self, horse_id: int) -> list[tuple]:
        if not isinstance(horse_id, int):
            raise IDError()

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

    def get_horses_with_age_in_range(self,
                                     age_from: str,
                                     age_to: str) -> list[tuple]:
        if not age_from:
            age_from = self._execute('SELECT MIN(age) FROM "Horse";')[0][0]
        
        if not age_to:
            age_to = self._execute('SELECT MAX(age) FROM "Horse";')[0][0]

        try:
            age_from = int(age_from)
            age_to = int(age_to)
        except ValueError:
            raise AgeError()

        return self._execute("""
            SELECT
                id, name
            FROM
                "Horse"
            WHERE
                age BETWEEN ? and ?
            ORDER BY age ASC;
        """, age_from, age_to)

    def get_races_with_horse(self, horse_id: int) -> list[tuple]:
        if not isinstance(horse_id, int):
            raise IDError()

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
        if not isinstance(race_id, int):
            raise IDError()
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

    def get_races_in_date_range(self, date_from: str, date_to: str) -> list[tuple]:
        if not date_from:
            date_from = self._execute('SELECT MIN(date) FROM "Race";')[0][0]
        else:
            date_from = date_from.strip()

        if not date_to:
            date_to = self._execute('SELECT MAX(date) FROM "Race";')[0][0]
        else:
            date_to = date_to.strip()

        if not DB.validate_date(date_from) or not DB.validate_date(date_to):
            raise DateError()
        
        return self._execute("""
            SELECT
                id, name
            FROM
                "Race"
            WHERE
                date BETWEEN DATE(?) and  DATE(?)
            ORDER BY date ASC;
        """, date_from, date_to)

    def get_race_results(self, race_id: int) -> list[tuple]:
        if not isinstance(race_id, int):
            raise IDError()

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
        if not isinstance(jockey_id, int):
            raise IDError()

        return self._execute("""
            SELECT
                name, age, address, rating
            FROM
                "Jockey"
            WHERE
                id = ?;
        """, jockey_id)

    def get_jockeys_races(self, jockey_id: int) -> list[tuple]:
        if not isinstance(jockey_id, int):
            raise IDError()

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

    def get_jockeys_with_rating_in_range(self, rating_from: str, rating_to: str) -> list[tuple]:
        if not rating_from:
            rating_from = self._execute('SELECT MIN(rating) FROM "Jockey";')[0][0]
        
        if not rating_to:
            rating_to = self._execute('SELECT MAX(rating) FROM "Jockey";')[0][0]
        
        try:
            rating_from = int(rating_from)
            rating_to = int(rating_to)
        except ValueError:
            raise JockeyRatingError()
        
        return self._execute("""
            SELECT
                id, name
            FROM
                "Jockey"
            WHERE
                rating BETWEEN ? and ?
            ORDER BY rating ASC;
        """, rating_from, rating_to)

    def get_hippodrome_races(self, hippodrome_id: int) -> list[tuple]:
        if not isinstance(hippodrome_id, int):
            raise IDError()

        return self._execute("""
            SELECT
                id, name
            FROM
                "Race"
            WHERE
                hippodrome_id = ?;
        """, hippodrome_id)

    def get_hippodrome_with_races_in_range(self,
                                           races_from: str,
                                           races_to: str) -> list[tuple]:
        if not races_from:
            races_from = self._execute("""
                SELECT
                    COUNT(r.id) as rc
                FROM
                    "Hippodrome" as h
                LEFT OUTER JOIN
                    "Race" as r
                ON
                    r.hippodrome_id = h.id
                GROUP BY h.id
                ORDER BY rc ASC
                LIMIT 1;
            """)[0][0]
        
        if not races_to:
            races_to = self._execute("""
                SELECT
                    COUNT(r.id) as rc
                FROM
                    "Hippodrome" as h
                LEFT OUTER JOIN
                    "Race" as r
                ON
                    r.hippodrome_id = h.id
                GROUP BY h.id
                ORDER BY rc DESC
                LIMIT 1;
            """)[0][0]

        try:
            races_from = int(races_from)
            races_to = int(races_to)
        except ValueError:
            raise CountValueError('Количество заездов')
        
        return self._execute("""
            SELECT
                h.id, h.name, COUNT(r.id) as rc
            FROM
                "Hippodrome" as h
            LEFT OUTER JOIN
                "Race" as r
            ON
                r.hippodrome_id = h.id
            GROUP BY h.id
            HAVING rc BETWEEN ? and ?
            ORDER BY rc ASC;
        """, races_from, races_to)

    def get_hippodrome(self, hippodrome_id: int) -> list[tuple]:
        if not isinstance(hippodrome_id, int):
            raise IDError()

        return self._execute("""
            SELECT
                name
            FROM
                Hippodrome
            WHERE
                id = ?;
        """, hippodrome_id)

    def delete_owner(self, owner_id: int):
        if not isinstance(owner_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Owner"
            WHERE id = ?;
        """, owner_id)

    def delete_horse(self, horse_id: int):
        if not isinstance(horse_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Horse"
            WHERE id = ?;
        """, horse_id)

    def delete_jockey(self, jockey_id: int):
        if not isinstance(jockey_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Jockey"
            WHERE id = ?;
        """, jockey_id)

    def delete_race(self, race_id: int):
        if not isinstance(race_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Race"
            WHERE id = ?;
        """, race_id)

    def delete_race_result(self, race_result_id: int):
        if not isinstance(race_result_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Race_result"
            WHERE id = ?;
        """, race_result_id)

    def delete_hippodrome(self, hippodrome_id: int):
        if not isinstance(hippodrome_id, int):
            raise IDError()

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
                         'Номер должен состоять из 11 цифр, начинаться с 8 или с +7,\n ' +
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


class CountValueError(Exception):
    def __init__(self, entity: str) -> None:
        super().__init__(f'{entity} должно быть представлено как целое \nнеотрицательное число')


class HippodromeNameError(NameError):
    def __init__(self, message_type: Union[Literal['incorrect_name'], Literal['name_not_unique']]) -> None:
        if message_type == 'incorrect_name':
            message = 'Название ипподрома не должно содержать числа.'
        else:
            message = 'Ипподром с таким названием уже существует'
        super().__init__(message)


class AgeError(Exception):
    def __init__(self, err_message: str = None) -> None:
        if err_message is None:
            err_message = 'Возраст должен быть представлен как целое неотрицательное число.'
        super().__init__('Неправильный формат возраста:\n'+err_message)


class JockeyAgeError(AgeError):
    def __init__(self) -> None:
        super().__init__('Возраст жокея должен быть представлен как целое число не меньшее 18.')


class JockeyRatingError(Exception):
    def __init__(self) -> None:
        super().__init__('Рейтинг должен быть представлен как целое неотрицательное число')


class DateError(Exception):
    def __init__(self) -> None:
        super().__init__('Неправильный формат даты:\nДолжен быть YYYY-MM-DD.')


class RaceResultPlaceError(Exception):
    def __init__(self) -> None:
        super().__init__('Занятое место должно быть целым числом в промежутке от 1 до 20.')


class RaceResultTimeError(Exception):
    def __init__(self) -> None:
        super().__init__('Время прибытия к финишу должно быть целым положительным числом.')


class IDError(Exception):
    def __init__(self) -> None:
        super().__init__('ID должен быть целым числом (int)')