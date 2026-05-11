import mysql.connector
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=False  # ← bas yeh ek line add karo
    )
    return connection