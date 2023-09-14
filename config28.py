API_TOKEN = '1982450546:AAHlsy4LeqGdybw4cJoMdiVIAosrAcomoSo'

import sqlite3
from pathlib import Path
import json
# class DBase:
    #
    # T_NAV_NAMES  = {'1': 'Навигатор Digma 100',
    #                 '2': 'Навигатор Garmin 150',
    #                 '3': 'Навигатор Garmin 120'}
    # T_NAV_PRICES = {'1': '5000',
    #                 '2': '14000',
    #                 '3': '12000'}
    #
    # def get_navigator_data(self, index_param):
    #     ret = "Данные не найдены!( Параметр:{}".format(index_param)
    #     index = int(index_param)
    #     if index == 0:
    #         ret = json.dumps(self.T_NAV_NAMES, ensure_ascii = False)
    #     elif index == 1:
    #         ret = json.dumps(self.T_NAV_PRICES, ensure_acii = False)
    #     return ret
class dbase_sql_lite:
    def __init__(self, name):
        self._name = name
        print(name)
        try:
            self._connect = self.sqllite_connect()
            c = self._connect.cursor()
            #c.execute('DROP TABLE IF EXISTS navigators')
            c.execute('CREATE TABLE navigators (nav_id INTEGER PRIMARY KEY, nav_name TEXT,\
            nav_price INTEGER)')
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

    def insert_data(self, id, name, price):
        db = Path("./{}.db".format(self._name))
        try:
            db.resolve(strict=True)
        except FileNotFoundError:
            print("База данных не найдена, сначала создайте!(")
            return -1
        try:
            c = self.sqlite_connect()
            if c == None:
                print("Подключение к базе данных SQL Lite не выполнено")
                return -2
            else:
                print("Подключение к базе данных SQL Lite успешно выполнено")
            c.execute('INSERT INTO navigator (nav_id, nav_name, nav_price) VALUES (?, ?, ?, ?)',\
                      (id, name, price))
            #c.execute('SELECT * FROM navigators')
            c.commit()
        except Exception as e:
            print("Ошибка при добавлении данных: ", e.__repr__(), e.args)
            return -3
        return 0
import sqlite3
import json

# DB = "./the_database.db"
#
# def get_all_users( json_str = False ):
#     conn = sqlite3.connect( DB )
#     conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
#     db = conn.cursor()
#
#     rows = db.execute('''
#     SELECT * from Users
#     ''').fetchall()
#
#     conn.commit()
#     conn.close()
#
#     if json_str:
#         return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON
#
#     return rows
if __name__=="__main__":
    dbase_sql_lite.sqlite_connect(self)
    dbase_sql_lite.insert_data(av,111,123,1000)