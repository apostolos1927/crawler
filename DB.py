import mysql.connector
from mysql.connector import Error


class connectDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost", database="test", user="....", password="...."
        )
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()

    def get_cursor(self):
        return self.cursor

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")
