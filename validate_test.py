import re
from datetime import datetime
from app.app import App
from app.db import DB

db = DB()
app = App(db)
app.run()

