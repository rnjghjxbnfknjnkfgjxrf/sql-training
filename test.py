from app.db import DB

db = DB()

print(db.get_jockeys_that_not_in_race(1))