import re
import sqlite3
from app.query_utils import INIT_DB_QUERY
from typing import Literal, Union
from datetime import datetime


class DB:
    """Класс, реализующий взаимодействие с БД"""
    __slots__ = ('_connection', '_cursor')

    def __init__(self, db_path: str = None):
        """
        Инициализация экземпляра класса:
        создание соединенияи выполнения
        запроса с инициализацией БД.

        :param db_path: путь к файлу с базой данных
                        (default 'app.db')
        """
        if db_path is None:
            db_path = 'app.db'
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()
        self._cursor.executescript(INIT_DB_QUERY)
        self._cursor.execute('PRAGMA foreign_keys = ON;')
        self._connection.commit()
        print('Connection created')

    def close_connection(self) -> None:
        """Закрывает соединение с БД."""
        self._cursor.close()
        self._connection.close()
        print('Connection closed')

    def _execute(self, query: str, *args) -> list[tuple]:
        """
        Выполнение заданного SQL запроса.

        :param query: запрос
        :type query: str

        :return: данные, полученные в результате
                 выполнения запроса.
        """
        try:
            res = self._cursor.execute(query, args)
            self._connection.commit()
        except Exception as err:
            raise DBExecuteQueryError(str(err))
        else:
            return res.fetchall()

    @staticmethod
    def validate_name(name: str) -> bool:
        """Валидация имени."""
        return re.match('^([а-я]+)$', name) is not None

    @staticmethod
    def validate_race_name(race_name: str) -> bool:
        """Валидация названия заезда."""
        return re.match('^([а-я][a-я ]*)$', race_name) is not None

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """Валидация номера телефона."""
        return re.match(
            '^(\+7|8)[ -]?[0-9]{3}[ -]?[0-9]{3}[ -]?([0-9]{2}[ -]?[0-9]{2}|[0-9]{4})$',
            phone_number) is not None

    @staticmethod
    def _parse_phone_number(phone_number: str) -> str:
        if phone_number.startswith('+'):
            return ''.join(re.split('[ -]', phone_number[2:]))
        else:
            return ''.join(re.split('[ -]', phone_number[1:]))

    @staticmethod
    def validate_date(date: str) -> bool:
        """Валидация даты."""
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def create_hippodrome(self, name: str) -> int:
        """
        Создание нового ипподрома.

        :param name: название
        :type name: str

        :raises HippodromeNameError: если имя не прошло
                                     валидацию или не
                                     является уникальным  

        :return: id созданного ипподрома
        """
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

    def create_owner(self, name: str, telephone: str, address: str) -> int:
        """
        Создание нового владельца.

        :param name: имя
        :type name: str
        :param telephone: номер телефона
        :type telephone: str
        :param address: address
        :type address: str

        :raises NameError: если имя не прошло валидацию
        :raises PhoneNumberError: если номер не прошел валидацию
                                  или не является уникальным

        :return: id созданного владельца
        """
        name = name.strip().lower()
        telephone.strip()

        if not DB.validate_name(name):
            raise NameError()
        elif not DB.validate_phone_number(telephone):
            raise PhoneNumberError('incorrect_phone')
        telephone = self._parse_phone_number(telephone)
        if any(telephone in x for x in self._execute('SELECT telephone FROM "Owner";')):
            raise PhoneNumberError('phone_not_unique')

        self._execute("""
            INSERT INTO "Owner" (name, telephone, address)
            VALUES (?, ?, ?);
        """, name.capitalize(), self._parse_phone_number(telephone), address)

        return self._cursor.lastrowid

    def create_horse(self,
                     name: str,
                     age: int,
                     gender: Union[Literal['мужской'], Literal['женский']],
                     owner_id: int) -> int:
        """
        Создание новой лошади.

        :param name: имя
        :type name: str
        :param age: возраст
        :type age: str
        :param gender: пол
        :type gender: str
        :param owner_id: id владельца
        :type owner_id: int

        :raises IDError: если id владельца не целое число
        :raises NameError: если имя не прошло валидацию
        :raises GenderError: если значение строки с полом
                             не равно "мужской" или "женский"
        :raises AgeError: если значение строки с возрастом
                          не является целым числом > 0

        :return: id созданного коня
        """
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
                     rating: str) -> int:
        """
        Создание нового жокея.

        :param name: имя
        :type name: str
        :param age: возраст
        :type age: str
        :param address: address
        :type address: str
        :param rating: рейтинг
        :type rating: str

        :raises NameError: если имя не прошло валидацию
        :raises JockeyAgeError: если значение строки с 
                                возрастом не равно целому
                                числу >= 18
        :raises JockeyRatingError: если значение строки с 
                                   рейтингом не равно целому
                                   числу >= 0

        :return: id созданного жокея
        """
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
                    hippodrome_id: int) -> int:
        """
        Создание нового заезда.

        :param name: название
        :type name: str
        :param date: дата
        :type date: str
        :param hippodrome_id: id ипподрома
        :type hippodrome_id: int

        :raises IDError: если id ипподрома не целое число
        :raises NameError: если название не прошло валидацию
        :raises DateError: если дата не прошла валидацию

        :return: id созданного заезда
        """
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
        """
        Создание нового результата заезда.

        :param result_place: занятое жокеем место
        :type result_place: str
        :param result_time: время, за которое жокей
                            добрался до финиша
        :type result_time: str
        :param race_id: id заезда
        :type race_id: int
        :param horse_id: id лошади
        :type horse_id: int
        :param jockey_id: id жокея
        :type jockey_id: int

        :raises IDError: если любой из переданных id не
                         является целым числом
        :raises RaceResultTimeError: если значение строки с временем
                                     результата не является целым
                                     числом > 0
        :raises RaceResultPlaceError: если значение строки с занятым
                                      местом не является целым
                                      числом в промежутке от 1 до 20
        :raises RaceResultCorrectnessError: если указанные жокей или 
                                            лошадь уже участвуют в данном
                                            заезде или указанное место
                                            уже занято
        """
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

        race_results = self._execute('SELECT jockey_id, horse_id, result_place FROM "Race_result";')

        if any(horse_id in x for x in race_results):
            raise RaceResultCorrectnessError('Указанная лошадь уже учавствует в этом заезде')
        elif any(jockey_id in x for x in race_results):
            raise RaceResultCorrectnessError('Указанный жокей уже учавствует в этом заезде')
        elif any(result_place in x for x in race_results):
            raise RaceResultCorrectnessError('В этом заезде данное место уже занято.')

        self._execute("""
            INSERT INTO "Race_result" (result_place, result_time, race_id, horse_id, jockey_id)
            VALUES (?, ?, ?, ?, ?);
        """, result_place, result_time, race_id, horse_id, jockey_id)        


    def get_all_horses(self) -> list[tuple]:
        """
        Получение всех лошадей

        :return: список кортежей из id и имен
        """
        return self._execute("""
            SELECT
                id, name
            FROM
                "Horse";
        """)

    def get_all_owners(self) -> list[tuple]:
        """
        Получение всех владельцев

        :return: список кортежей из id и имен
        """
        return self._execute("""
            SELECT
                id, name
            FROM
                "Owner";
        """)

    def get_all_jockeys(self) -> list[tuple]:
        """
        Получение всех жокеев

        :return: список кортежей из id и имен
        """
        return self._execute("""
            SELECT
                id, name
            FROM
                "Jockey";
        """)

    def get_all_races(self) -> list[tuple]:
        """
        Получение всех заездов

        :return: список кортежей из id и имен
        """
        return self._execute("""
            SELECT
                id, name
            FROM
                "Race";
        """)

    def get_all_hippodromes(self) -> list[tuple]:
        """
        Получение всех ипподромов

        :return: список кортежей из id и имен
        """
        return self._execute("""
            SELECT
                id, name
            FROM
                "Hippodrome";
        """)

    def get_jockeys_that_not_in_race(self, race_id: int) -> list[tuple]:
        """
        Получение жокеев, которые не участвуют в
        указанном заезде.

        :param race_id: id заезда
        :type race: int

        :raises IDError: если id заезда не целое
                         число
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение лодашей, которые не участвуют в
        указанном заезде.

        :param race_id: id заезда
        :type race: int

        :raises IDError: если id заезда не целое
                         число
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение информации об указанном владельце.

        :param owner_id: id владельца
        :type owner_id: int

        :raises IDError: если id владельца не целое
                         число

        :return: список с кортежем из имени, адреса
                 и номера мобильного телефона
        """
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
        """
        Получение лошадей, принадлежащих указанному
        владельцу.

        :param owner_id: id владельца
        :type owner_id: int

        :raises IDError: если id владельца не целое
                         число

        :return: список кортежей из id и имен
        """
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
        """
        Получение владельцев, у которых количество
        лошадей находится в указанном диапазоне.
        Если начало или конец промежутка не указаны
        (передана пустая строка),то им присваиваются
        минимальное/максимальное значения соответственно.

        :param horses_from: начало промежутка
        :type horses_from: str
        :param horses_to: конец промежутка
        :type horses_to: str

        :raises CountValueError: если значение строки с
                                 границей промежутка не
                                 является целым числом
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение информации об указанном коне.

        :param horse_id: id владельца
        :type horse_id: int

        :raises IDError: если id лошади не целое
                         число

        :return: список с кортежем из имени, возраста и
                 пола коня, имени и id владельца 
        """
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
        """
        Получение коней, у которых возраст находится 
        в указанном диапазоне.
        Если начало или конец промежутка не указаны
        (передана пустая строка),то им присваиваются
        минимальное/максимальное значения соответственно.

        :param age_from: начало промежутка
        :type age_from: str
        :param age_to: конец промежутка
        :type age_to: str

        :raises AgeError: если значение строки с
                          границей промежутка не
                          является целым числом
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение заездов, в которых учавствовала
        указанная лошадь.

        :param horse_id: id коня
        :type horse_id: int

        :raises IDError: если id лошади не целое
                         число

        :return: список кортежей из id и имен
        """
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
        """
        Получение информации об указанном заезде.

        :param race_id: id заезда
        :type race_id: int

        :raises IDError: если id заезда не целое
                         число

        :return: список с кортежем из имени и даты
                 заезда, имени и id ипподрома 
        """
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
        """
        Получение заездов дата проведения которых
        лежит в указанном промежутке.
        Если начало или конец промежутка не указаны
        (передана пустая строка),то им присваиваются
        минимальное/максимальное значения соответственно.

        :param date_from: начало промежутка
        :type date_from: str
        :param date_to: конец промежутка
        :type date_to: str

        :raises CountValueError: если значение строки с
                                 границей промежутка не
                                 является целым числом
        :raises DateError: если даты не прошли валидацию

        :return: список кортежей из id и имен
        """
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
        """
        Получение результатов указанного заезда.

        :param race_id: id заезда
        :type race_id: int

        :raies IDError: если id заезда не
                        является целым числом

        :return: список с кортежем из id, места
                 и времени резульата, имени и id жокея,
                 имени и id коня
        """
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
        """
        Получение информации об указанном жокее.

        :param jockey_id: id жокея
        :type jockey_id: int

        :raises IDError: если id жокея не целое
                         число

        :return: список с кортежем из имени, возраста,
                 адреса и рейтинга жокея
        """
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
        """
        Получение заездов, в которых учавствовал
        указанный жокей.

        :param jockey_id: id коня
        :type jockey_id: int

        :raises IDError: если id жокея не целое
                         число

        :return: список кортежей из id и имен
        """
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
        """
        Получение жокеев, рейтинг которых находится
        в указанном диапазоне.
        Если начало или конец промежутка не указаны
        (передана пустая строка),то им присваиваются
        минимальное/максимальное значения соответственно.

        :param rating_from: начало промежутка
        :type rating_from: str
        :param rating_to: конец промежутка
        :type rating_to: str

        :raises JockeyRatingError: если значение строки с
                                   границей промежутка не
                                   является целым числом
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение заездов, проведенных на указанном
        ипподроме.

        :param hippodrome_id: id коня
        :type hippodrome_id: int

        :raises IDError: если id ипподрома не целое
                         число

        :return: список кортежей из id и имен
        """
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
        """
        Получение ипподромов, количество проведенных
        заездов на которых находится в указанном
        промежутке.
        Если начало или конец промежутка не указаны
        (передана пустая строка),то им присваиваются
        минимальное/максимальное значения соответственно.

        :param races_from: начало промежутка
        :type races_from: str
        :param races_to: конец промежутка
        :type races_to: str

        :raises CountValueError: если значение строки с
                                 границей промежутка не
                                 является целым числом
        
        :return: список кортежей из id и имен
        """
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
        """
        Получение информации об указанном ипподроме.

        :param hippodrome_id: id ипподрома
        :type hippodrome_id: int

        :raises IDError: если id лошади не целое
                         число

        :return: список с кортежем из имени ипподрома. 
        """
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

    def delete_owner(self, owner_id: int) -> None:
        """
        Удаление указанного владельца.

        :param owner_id: id владельца
        :type owner_id: int

        :raises IDError: если id владельца
                         не целое число
        """
        if not isinstance(owner_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Owner"
            WHERE id = ?;
        """, owner_id)

    def delete_horse(self, horse_id: int) -> None:
        """
        Удаление указанного коня.

        :param horse_id: id лошади
        :type horse_id: int

        :raises IDError: если id коня
                         не целое число
        """
        if not isinstance(horse_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Horse"
            WHERE id = ?;
        """, horse_id)

    def delete_jockey(self, jockey_id: int) -> None:
        """
        Удаление указанного жокея.

        :param jockey_id: id жокея
        :type jockey_id: int

        :raises IDError: если id жокея
                         не целое число
        """
        if not isinstance(jockey_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Jockey"
            WHERE id = ?;
        """, jockey_id)

    def delete_race(self, race_id: int) -> None:
        """
        Удаление указанного заезда.

        :param race_id: id заезда
        :type race_id: int

        :raises IDError: если id заезда
                         не целое число
        """
        if not isinstance(race_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Race"
            WHERE id = ?;
        """, race_id)

    def delete_race_result(self, race_result_id: int) -> None:
        """
        Удаление указанного результата заезда.

        :param race_result_id: id результата заезда
        :type race_result_id: int

        :raises IDError: если id результата заезда
                         не целое число
        """
        if not isinstance(race_result_id, int):
            raise IDError()

        self._execute("""
            DELETE FROM "Race_result"
            WHERE id = ?;
        """, race_result_id)

    def delete_hippodrome(self, hippodrome_id: int) -> None:
        """
        Удаление указанного ипподрома.

        :param hippodrome_id: id ипподрома
        :type hippodrome_id: int

        :raises IDError: если id ипподрома
                         не целое число
        """
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
    def __init__(self, message_type: Union[Literal['incorrect_phone'], Literal['phone_not_unique']]) -> None:
        if message_type == 'incorrect_name':
            message = 'Неправильный формат номера телефона:\n' +\
                      'Номер должен состоять из 11 цифр, начинаться с 8 или с +7,\n ' +\
                      'в качестве разделителей можно использовать пробел или знак тире.'
        else:
            message = 'Владелец с таким номера телефона уже существует'
        super().__init__(message)


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


class RaceResultCorrectnessError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RaceResultTimeError(Exception):
    def __init__(self) -> None:
        super().__init__('Время прибытия к финишу должно быть целым положительным числом.')


class IDError(Exception):
    def __init__(self) -> None:
        super().__init__('ID должен быть целым числом (int)')