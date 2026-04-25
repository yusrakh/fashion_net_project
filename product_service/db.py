import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="fashion_net"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise