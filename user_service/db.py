import mysql.connector
import os

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'fashion-net-2026-dc.mysql.database.azure.com'),
            user=os.environ.get('DB_USER', 'yusrakhalid8'),
            password=os.environ.get('DB_PASSWORD', 'Joakmn095'),
            database=os.environ.get('DB_NAME', 'fashion_net'),
            ssl_disabled=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise