import sqlite3


class DBHandler(object):

    def __init__(self, dbpath=None):
        try:
            self.db_connection = sqlite3.connect(dbpath)
            self.db = self.db_connection.cursor()
            print("Connected to SQLite")
        except:
            #TODO
            print("error")

    def get_all_values_from_column(self, table_name, colume_name):
        try:

            sqlite_select_query = "SELECT " + colume_name + " from " + table_name
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            all_values = []
            for row in records:
                all_values.append(row[0])

            return all_values

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

    def get_value_from_column_by_id(self, table_name, colume_name, id):
        try:
            sqlite_select_query = "SELECT " + colume_name + " from " + table_name + " WHERE ID = " + id
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            result = records[0][0]
            return result
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

    def update_table(self, table_name, column_name, id, column_name_value):
        try:
            sqlite_insert_query = "UPDATE " + table_name +  " SET " + column_name + " = " + column_name_value + " WHERE ID = " + id
            self.db.execute(sqlite_insert_query)
            self.db_connection.commit()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

    def get_supplier_from_company(self, company_name):
        try:
            sqlite_select_query = "SELECT * from company_supplier where company = \"" + company_name + "\""
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            if len(records) == 1:
                row = records[0]
                return row[2]
            else:
                return None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return None

    def get_sender_hint(self, company_name):
        try:
            sqlite_select_query = "SELECT * from company_supplier where company = \"" + company_name + "\""
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            if len(records) == 1:
                row = records[0]
                return row[3]
            else:
                return None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return None

    def get_supplier_hint(self, slug):
        try:
            sqlite_select_query = "SELECT * from suppliers where slug = \"" + slug + "\""
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            if len(records) == 1:
                row = records[0]
                return row[4]
            else:
                return None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return None

    def get_supplier_name(self, domain):
        try:
            sqlite_select_query = "SELECT * from suppliers where mail_domain = \"" + domain + "\""
            self.db.execute(sqlite_select_query)
            records = self.db.fetchall()
            if len(records) == 1:
                row = records[0]
                return row[2]
            else:
                return None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return None

    def close_connection(self):
        self.db.close()
        if self.db_connection:
            self.db_connection.close()
            print("The SQLite connection is closed")