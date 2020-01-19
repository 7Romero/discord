import mysql.connector

def connectBD():
    mydb = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database=""
        )

    return mydb
