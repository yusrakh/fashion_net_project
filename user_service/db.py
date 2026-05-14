import mysql.connector
import os

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get(
                'DB_HOST',
                'fashion-net-2026-dc.mysql.database.azure.com'
            ),

            user=os.environ.get(
                'DB_USER',
                'yusrakhalid8@fashion-net-2026-dc'
            ),

            password=os.environ.get(
                'DB_PASSWORD',
                'Joakmn095'
            ),

            database=os.environ.get(
                'DB_NAME',
                'fashion_net'
            ),

            port=3306,

            ssl_disabled=False,
            ssl_verify_cert=False,
            ssl_verify_identity=False
        )

        return connection

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise