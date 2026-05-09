import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="fashion-net-2026-dc.mysql.database.azure.com",
            user="yusrakhalid8",
            password="Joakmn095",
            database="fashion_net",
            ssl_disabled=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise