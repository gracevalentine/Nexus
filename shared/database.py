import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="nexusdb2"
    )
    return db
