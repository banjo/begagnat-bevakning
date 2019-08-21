import mysql.connector
import os

# get auth variables
SQL_HOST = os.environ.get("SQL_HOST")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASS = os.environ.get("SQL_PASS")

# connect to database
db = mysql.connector.connect(host=SQL_HOST,
                             user=SQL_USER,
                             passwd=SQL_PASS,
                             database="begagnat")


def add_id_to_blocket(id):
    cursor = db.cursor()
    sql = "INSERT INTO blocket (id, has_viewed) VALUES (%s, %s)"
    val = (id, 1)
    cursor.execute(sql, val)
    db.commit()


def check_id_for_blocket(item_id):
    cursor = db.cursor()
    sql = "SELECT id FROM blocket WHERE id = %s"
    val = (item_id, )
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def add_id_to_tradera(id):
    cursor = db.cursor()
    sql = "INSERT INTO tradera (id, has_viewed) VALUES (%s, %s)"
    val = (id, 1)
    cursor.execute(sql, val)
    db.commit()


def check_id_for_tradera(item_id):
    cursor = db.cursor()
    sql = "SELECT id FROM tradera WHERE id = %s"
    val = (item_id, )
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False
