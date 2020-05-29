import sqlite3


class DBHandler(object):

    global db
    global db_connection

    def __init__(self, dbpath):
        try:
            db_connection = sqlite3.connect(dbpath)
            db = db_connection.cursor()
            print("Connected to SQLite")
        except:
            #TODO
            print("error")


    def get_all_values_from_column(self, table_name, colume_name):
        try:

            sqlite_select_query = "SELECT " + colume_name + " from " + table_name
            db.execute(sqlite_select_query)
            records = db.fetchall()

            for row in records:
                print("Id: ", row[0])


            db.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if db_connection:
                db_connection.close()
                print("The SQLite connection is closed")
