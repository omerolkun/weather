from html import entities
from pyowm.owm import OWM
import datetime
from datetime import date
import time
import sqlite3
from sqlite3 import Error
import datetime
import schedule
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_insert(db_name,date, temperature):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_table_query = "create table if not exists weather_table (date text,temperature int);"
    cursor.execute(create_table_query)
    query = "insert into weather_table (date,temperature) values (?,?);"
    data = (date, temperature)
    cursor.execute(query,data)
    
    conn.commit()

def weather():
    x = datetime.datetime.now()

    month = x.strftime("%B")
    day = x.strftime("%d")
    year = x.strftime("%Y")
    hour = x.strftime("%H")
    minute = x.strftime("%M")

    date = day + " "+ month + " " + year + " " + hour + ":" + minute  

    apikey =  ###
    owm = OWM(apikey)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('Ankara').weather  

    temp_dict_celsius = weather.temperature('celsius')  #

    felt_temp =temp_dict_celsius['feels_like'] 
    felt_temp = int(felt_temp)

    create_connection("weather.db")

    create_insert("weather.db",date ,felt_temp)

schedule.every().day.at("7:00").do(weather)
schedule.every().day.at("12:00").do(weather)
schedule.every().day.at("18:00").do(weather)
schedule.every().day.at("13:00").do(weather)


while True:
    schedule.run_pending()
    time.sleep(1)