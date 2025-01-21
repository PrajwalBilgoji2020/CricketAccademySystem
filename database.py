import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kalpesh@01",
        database="cricket_academy"
    )

def execute_query(query, values=None):
    db = connect()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

def fetch_data(query, values=None):
    db = connect()
    cursor = db.cursor()
    cursor.execute(query, values)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data
