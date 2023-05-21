from app.db import DB
from app.query_utils import INIT_DB_QUERY

db = DB()
# db.create_hippodrome('болото')
# db.create_owner('иван', '+79605455587', 'Yarik')
# db.create_horse('яков', 7, 'мужской', 1)
# db.create_joсkey('петр', 18, 'Moscow', 5)
# db.create_race('большая гонка', '2022-06-12', 1)
# db.create_race_result('2', 12, 1, 1, 1)

print(db.get_race(1))

db.close_connection()