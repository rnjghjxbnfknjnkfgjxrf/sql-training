INIT_DB_QUERY = """CREATE TABLE IF NOT EXISTS "Hippodrome"(
                 id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 PRIMARY KEY (id),
                 UNIQUE (name)
                 );

                 CREATE TABLE IF NOT EXISTS "Race"(
                 id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 date TEXT NOT NULL,
                 hippodrome_id INTEGER NOT NULL,
                 PRIMARY KEY (id),
                 FOREIGN KEY (hippodrome_id) REFERENCES "Hippodrome" ON DELETE CASCADE
                 );

                 CREATE TABLE IF NOT EXISTS "Jockey"(
                 id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 address TEXT NOT NULL,
                 rating INTEGER NOT NULL,
                 PRIMARY KEY (id),
                 CHECK (age >= 18),
                 CHECK (rating >= 0)
                 );
                 
                 CREATE TABLE IF NOT EXISTS "Owner"(
                 id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 telephone TEXT NOT NULL,
                 address TEXT NOT NULL,
                 PRIMARY KEY (id),
                 UNIQUE (telephone)
                 );
                 
                 CREATE TABLE IF NOT EXISTS "Horse"(
                 id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 gender TEXT NOT NULL,
                 owner_id INTEGER NOT NULL,
                 PRIMARY KEY (id),
                 FOREIGN KEY (owner_id) REFERENCES "Owner" ON DELETE CASCADE,
                 CHECK (age >= 0),
                 CHECK (gender in (\'женский\', \'мужской\'))
                 );
                 
                 CREATE TABLE IF NOT EXISTS "Race_result"(
                 id INTEGER NOT NULL,
                 result_place INTEGER NOT NULL,
                 result_time INTEGER NOT NULL,
                 race_id INTEGER NOT NULL,
                 horse_id INTEGER NOT NULL,
                 jockey_id INTEGER NOT NULL,
                 PRIMARY KEY (id),
                 FOREIGN KEY (race_id) REFERENCES "Race" ON DELETE CASCADE,
                 FOREIGN KEY (horse_id) REFERENCES "Horse" ON DELETE CASCADE,
                 FOREIGN KEY (jockey_id) REFERENCES "Jockey" ON DELETE CASCADE,
                 CHECK (result_place > 0),
                 CHECK (result_time > 0),
                 UNIQUE (jockey_id),
                 UNIQUE (horse_id)
                 );"""