import mysql.connector
from fastapi import HTTPException


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            database='db',
            host='mysql',
            port='3306',
            user='root',
            password='root'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(status_code=404, detail="Database not found")
        else:
            raise HTTPException(
                status_code=500, detail=f"Error connecting to database: {err}")
