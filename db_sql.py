import sqlite3
from pathlib import Path

class dbase_sql_lite:
    def __init__(self, name):
        self._name = name
        try:
            self._connect = self.sqllite_connect()
            c = self._connect.cursor()
            c.execute('CREATE TABLE proverb (prov_id INTEGER PRIMARY KEY, proverbs TEXT)')
            self._connect.commit()
            self._connect.close()
        except Exception as e:
            print("Ошибка при создании базы данных: ", e.__repr__(), e.args)
            pass
        print("База данных успешно создана!!")


    def sqlite_connect(self):
        self._connect = sqlite3.connect("{}.db".format(self._name), check_same_thread=False)
        self._connect.execute("pragma journal_mode=wal;")
        return self._connect

    def insert_data(self, id, name):
        db = Path("./{}.db".format(self._name))
        try:
            db.resolve(strict=True)
        except FileNotFoundError:
            print("База данных не найдена, сначала создайте!")
            return -1
        try:
            c = self.sqlite_connect()
            if c == None:
                print("Подключение к базе данных SQL Lite не выполнено")
                return -2
            else:
                print("Подключение к базе данных SQL Lite успешно выполнено")
            c.execute('INSERT INTO proverb (prov_id, proverbs) VALUES (?, ?)',\
                      (id, name))
            c.commit()
        except Exception as e:
            print("Ошибка при добавлении данных: ", e.__repr__(), e.args)
            return -3
        return 0