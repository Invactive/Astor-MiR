import mysql.connector
import get_save_data as gsd
import sys
import guli


def createDatabase(host, user, passwd):
    # Create database and tables MySQL
    try:
        db = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd)
        cursor = db.cursor()
    except:
        print("Database connection error!")
        sys.exit("Database connection error!")

    cursor.execute("CREATE DATABASE IF NOT EXISTS MIR_DB")
    cursor.execute("USE MIR_DB")

    create_robots = ('CREATE TABLE IF NOT EXISTS robots('
                     'id INT NOT NULL AUTO_INCREMENT,'
                     'name VARCHAR(255) NOT NULL,'
                     'model VARCHAR(255) NOT NULL,'
                     'serial_num VARCHAR(255) NOT NULL,'
                     'map_id VARCHAR(255) NOT NULL,'
                     'timestamp VARCHAR(255) NOT NULL,'
                     'PRIMARY KEY (id),'
                     'UNIQUE (serial_num));')
    cursor.execute(create_robots)

    create_maps = ('CREATE TABLE IF NOT EXISTS maps('
                   'id INT NOT NULL AUTO_INCREMENT,'
                   'name VARCHAR(255) NOT NULL,'
                   'guid VARCHAR(255) NOT NULL,'
                   'url VARCHAR(512) NOT NULL,'
                   'timestamp VARCHAR(255) NOT NULL,'
                   'PRIMARY KEY (id),'
                   'UNIQUE (guid));')
    cursor.execute(create_maps)

    create_robots_live_data = ('CREATE TABLE IF NOT EXISTS robots_live_data('
                               'id INT NOT NULL AUTO_INCREMENT,'
                               'name VARCHAR(255) NOT NULL,'
                               'battery FLOAT,'
                               'battery_time_remain INT,'
                               'uptime INT,'
                               'state VARCHAR(255) NOT NULL,'
                               'distance FLOAT,'
                               'errors VARCHAR(2048),'
                               'mission VARCHAR(255),'
                               'timestamp VARCHAR(255) NOT NULL,'
                               'PRIMARY KEY (id));')
    cursor.execute(create_robots_live_data)
    cursor.execute('TRUNCATE robots_live_data')

    create_positions = ('CREATE TABLE IF NOT EXISTS positions('
                        'id INT NOT NULL AUTO_INCREMENT,'
                        'name VARCHAR(255) NOT NULL,'
                        'guid VARCHAR(255) NOT NULL,'
                        'created_by_name VARCHAR(255) NOT NULL,'
                        'created_by_id VARCHAR(255) NOT NULL,'
                        'map_id VARCHAR(255) NOT NULL,'
                        'pos_x FLOAT,'
                        'pos_y FLOAT,'
                        'orientation FLOAT,'
                        'timestamp VARCHAR(255) NOT NULL,'
                        'PRIMARY KEY (id),'
                        'UNIQUE (guid));')
    cursor.execute(create_positions)

    create_software_logs = ('CREATE TABLE IF NOT EXISTS software_logs('
                            'id INT NOT NULL AUTO_INCREMENT,'
                            'guid VARCHAR(255) NOT NULL,'
                            'from_ver VARCHAR(255) NOT NULL,'
                            'to_ver VARCHAR(255) NOT NULL,'
                            'state VARCHAR(255) NOT NULL,'
                            'action VARCHAR(255) NOT NULL,'
                            'start_time VARCHAR(255) NOT NULL,'
                            'end_time VARCHAR(255) NOT NULL,'
                            'PRIMARY KEY (id),'
                            'UNIQUE (guid));')
    cursor.execute(create_software_logs)

    create_error_logs = ('CREATE TABLE IF NOT EXISTS error_logs('
                        'id INT NOT NULL,'
                        'description VARCHAR(2048),'
                        'module VARCHAR(255) NOT NULL,'
                        'download_url VARCHAR(255) NOT NULL,'
                        'time VARCHAR(255) NOT NULL,'
                        'PRIMARY KEY (id),'
                        'UNIQUE (download_url));')
    cursor.execute(create_error_logs)

    db.commit()
    print("Database and tables created successfuly!")

    return db, cursor

# initLoad runs once at the beginning
def initLoad(host, user, passwd):
    try:
        db = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd)
        cursor = db.cursor()
    except:
        print("Database connection error!")
        sys.exit("Database connection error!")

    fileVariable = open('live_data.csv', 'r+')
    fileVariable.truncate(0)
    fileVariable.close()
    cursor.execute("USE MIR_DB;")
    cursor.execute("TRUNCATE robots_live_data;")

    gsd.getRobotOverview(db, cursor)
    gsd.getRobotLiveData(db, cursor)
    gsd.getFromMirDB(db, cursor)
    guli.GuliVariable("Init").setValue('1')
    gsd.getMaps(db, cursor)
    gsd.getPosDetails(db, cursor)
    gsd.getSoftwareLogs(db, cursor)
    gsd.getErrorLogs(db, cursor)

