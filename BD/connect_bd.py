import mysql.connector

def connectBD():
    mydb = mysql.connector.connect(
        host="149.202.88.165",
        user="gs47360",
        passwd="GcmVAyvNCh6L",
        database="gs47360"
        )

    return mydb
