import sqlite3
import os

try:
    basedir = os.path.abspath(os.path.dirname(__file__))
    strDatabase = os.path.join(basedir, 'quizz.sqlite3')
    strScript = os.path.join(basedir, 'script.sql')

    sqliteConnection = sqlite3.connect(strDatabase)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    with open(strScript, 'r') as sqlite_file:
        sql_script = sqlite_file.read()

    cursor.executescript(sql_script)
    print("SQLite script executed successfully")
    cursor.close()

except sqlite3.Error as error:
    print("Error while executing sqlite script", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")