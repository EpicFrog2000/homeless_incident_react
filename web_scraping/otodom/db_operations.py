import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="otodom_db",
)

todays_date = datetime.datetime.now()
todays_date = str(todays_date.year) + "-" + str(todays_date.month)  + "-" + str(todays_date.day)


def insert_data(oferta):
    connection = mydb.cursor()
    print(oferta.lokacja)
    # Add db operations...