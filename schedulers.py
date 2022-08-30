import schedule
import mysql.connector
import get_save_data as gsd
import time
import guli
import sys


def dbScheduler(host, user, passwd):
    try:
        db = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd)
        cursor = db.cursor()
    except:
        print("Database connection error!")
        sys.exit("Database connection error!")

    schedule.every(2).minutes.do(gsd.getRobotOverview, db=db, cursor=cursor)

    # Battery logger
    schedule.every().second.do(gsd.getRobotLiveData, db=db, cursor=cursor)
    schedule.every(2).seconds.do(gsd.getFromMirDB, db=db, cursor=cursor) # converts RobotLiveData to csv

    # To DB
    schedule.every().minute.do(gsd.getMaps, db=db, cursor=cursor)
    schedule.every().minute.do(gsd.getPosDetails, db=db, cursor=cursor)
    schedule.every().minute.do(gsd.getSoftwareLogs, db=db, cursor=cursor)
    schedule.every(30).seconds.do(gsd.getErrorLogs, db=db, cursor=cursor)

    while True:
        schedule.run_pending()
        time.sleep(1)
        # When app shut down, clear jobs from schedule, close cursor and db connection
        try:
            if guli.GuliVariable("winClosed").get():
                schedule.clear()
                cursor.close()
                db.close()
                break
        except:
            pass
