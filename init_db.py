import sqlite3

def init_database():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()
