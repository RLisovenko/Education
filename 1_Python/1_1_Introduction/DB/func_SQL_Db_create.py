import sqlite3
from sqlite3 import Error
con = sqlite3.connect("tutorial.db")

"""
Використання вбудованої бібліотеки Python sqlite3 для роботи з БД SQLite.
https://docs.python.org/3/library/sqlite3.html
"""
class cls_DB_func():
    """
    function arbeit mit class  з БД.
    """
    def __init__(self, strFilePathDB = "./data/sqliteDB", strDefault_type_db = "SQlLite"):
        self.filePathDb = strFilePathDB
        self.default_type_db = strDefault_type_db
        self.db_con = None
        self.db_cursor = None
        self.strSql_execute = "CREATE TABLE IF NOT EXISTS test_users2 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"

    def cls_func_create_con(self):
        """
        :param path:wo ist file SQlLiteDb
        :return: connection an database
        """
        #DB_connection = None
        try:
            self.db_con = sqlite3.connect(self.filePathDb)
            self.db_cursor = self.db_con.cursor
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return  self.db_con

    def cls_execute_query(self , db_con, strSqlQuery = ""):
        self.db_cursor = db_con.cursor()
        try:
            self.db_cursor.execute(strSqlQuery)
            self.db_con.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")


    def cls_execute_read_query(self,db_con, strSqlQuery):
        self.db_cursor = db_con.cursor()
        result = None
        try:
            self.db_cursor.execute(strSqlQuery)
            result = self.db_cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    def cls_return_rows_items(self, db_conn,strSqlQuery):
        tmp_collection = cls_execute_read_query(db_conn, strSqlQuery)
        for tmp_item in tmp_collection:
            print(tmp_item)
        return  tmp_collection

#-------------------------

# D:\DB\Seminar\Db_example\sql\webinar_sql_python_2022_12_5-7\data\
#my_db_con = myFunc_create_connection("D:/DB/Seminar/Db_example/sql/webinar_sql_python_2022_12_5-7/data/sqliteDB")

my_db = cls_DB_func("D:/DB/Seminar/Db_example/sql/webinar_sql_python_2022_12_5-7/data/sqliteDB","sqlite")
my_db_con = my_db.cls_func_create_con()

my_db.cls_execute_query(my_db_con,"CREATE TABLE IF NOT EXISTS test_users2 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
myResDbList = my_db.cls_execute_read_query(my_db_con,"SELECT name FROM sqlite_master")

print("myResDbList",myResDbList)
#my_db.cls_return_rows_items(my_db_con,"SELECT * from users")
tmp_collection = my_db.cls_execute_read_query(my_db_con, "SELECT * from users")
for tmp_item in tmp_collection:
    print(tmp_item)






