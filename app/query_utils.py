INIT_DB_QUERY = """
                CREATE TABLE IF NOT EXISTS "Hippodrome"(
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
                CHECK (result_place BETWEEN 1 and 20),
                CHECK (result_time > 0),
                UNIQUE (jockey_id),
                UNIQUE (horse_id)
                );

                CREATE TRIGGER IF NOT EXISTS check_is_race_result_correct
                BEFORE INSERT ON "Race_result"
                BEGIN
                    WITH 
                        jockeys_in_race AS (SELECT jockey_id),
                        horses_in_race AS (SELECT horse_id),
                        places_in_race AS (SELECT result_place)
                    SELECT 
                        CASE
                            WHEN (NEW.result_place) IN places_in_race THEN (RAISE(ABORT, 'В этом заезде данное место уже занято.'))
                            WHEN (NEW.jockey_id) IN jockeys_in_race THEN (RAISE(ABORT, 'Указанный жокей уже учавствует в этом заезде'))
                            WHEN (NEW.horse_id) in horses_in_race THEN (RAISE(ABORT, 'Указанная лошадь уже учавствует в этом заезде'))
                        END
                    FROM "Race_result";
                END;

                CREATE TRIGGER IF NOT EXISTS update_jockey_rating 
                AFTER INSERT ON "Race_result"
                BEGIN
                    UPDATE "Jockey"
                    SET rating = (CASE
                                    WHEN (NEW.result_place = 1) THEN (rating + 50)
                                    WHEN (NEW.result_place = 2) THEN (rating + 25)
                                    WHEN (NEW.result_place = 3) THEN (rating + 15)
                                    WHEN (NEW.result_place IN (4, 10)) THEN (rating + 5)
                                    WHEN (NEW.result_place > 10) THEN (rating + 1)
                                  END)
                    WHERE
                        id = NEW.jockey_id;
                END;
                
                CREATE TRIGGER IF NOT EXISTS check_race_date
                BEFORE INSERT ON "Race"
                WHEN 
                    EXISTS (
                            SELECT id
                            FROM "Race"
                            WHERE
                                date = NEW.date AND hippodrome_id = NEW.hippodrome_id
                    )
                BEGIN
                    SELECT RAISE(ABORT, 'Нельзя создавать заезд с указанной датой на данном ипподроме, т.к. это время занято');
                END;
                """
