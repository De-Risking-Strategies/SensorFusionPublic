import sqlite3


def drop_table():
    with sqlite3.connect('sf.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS user;""")
    return True


def create_db():
    with sqlite3.connect('sf.db') as connection:
        c = connection.cursor()
        table = """CREATE TABLE user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            email TEXT NOT NULL,
            captureLimit INTEGER NOT NULL
        );
        """
        c.execute(table)
    return True


if __name__ == '__main__':
    drop_table()
    create_db()
