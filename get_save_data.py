import requests
from datetime import datetime
import csv
import login_data as ld
import user_exceptions as ue
import guli


'''
Classes and functions for getting data from MIR REST API and saving them in MySQL database.
'''

# Getting robot data
class Robot:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def getRobotOverview(db, cursor):
    # Getting robot's overview
    try:
        getRobotStatus = requests.get (ld.MIR_host + 'status' , headers = ld.MIR_headers)
        match getRobotStatus.status_code:
            case 200:
                robotStatusJson = getRobotStatus.json()
                robotStatusJson = [robotStatusJson] # Temp solution instead of robots fromm MIR Fleet (len = 1)
                for i in range(len(robotStatusJson)):
                    tempRobot = Robot(**robotStatusJson[i])
                    cursor.execute('USE MIR_DB')
                    robot_values = ('INSERT IGNORE INTO robots (name, model, serial_num, map_id, timestamp) '
                                    f'VALUES (\'{tempRobot.robot_name}\', \'{tempRobot.robot_model}\','
                                    f'\'{tempRobot.serial_number}\', \'{tempRobot.map_id}\','
                                    f'\'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\');')
                    cursor.execute(robot_values)
                    db.commit()
                print(f'Added {len(robotStatusJson)} robots to database.')
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting maps - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting robot overview - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting robot overview.")
        print("Error not defined.")
    finally:
        getRobotStatus.close()

def getRobotLiveData(db, cursor):
    # Getting robot's live data
    try:
        getRobotLive = requests.get(ld.MIR_host + 'status' , headers = ld.MIR_headers)
        match getRobotLive.status_code:
            case 200:
                robotLiveJson = getRobotLive.json()
                robotLiveJson = [robotLiveJson] # Temp solution instead of robots fromm MIR Fleet (len = 1)
                for i in range(len(robotLiveJson)):
                    tempRobotLive = Robot(**robotLiveJson[i])
                    tempRobotLive.mission_text = tempRobotLive.mission_text.replace("'","")
                    cursor.execute('USE MIR_DB')
                    robotLive_values = ('INSERT INTO robots_live_data (name, battery, battery_time_remain, uptime, state,'
                                        'distance, errors, mission, timestamp)'
                                        f'VALUES (\'{tempRobotLive.robot_name}\', \'{tempRobotLive.battery_percentage}\','
                                        f'\'{tempRobotLive.battery_time_remaining}\', \'{tempRobotLive.uptime}\','
                                        f'\'{tempRobotLive.state_text}\', \'{tempRobotLive.moved}\','
                                        f'\'{tempRobotLive.errors}\', \'{tempRobotLive.mission_text}\','
                                        f'\'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\');')
                    cursor.execute(robotLive_values)
                    try:
                        guli.GuliVariable("robotName").setValue(tempRobotLive.robot_name)
                        guli.GuliVariable("battery").setValue(tempRobotLive.battery_percentage)
                        guli.GuliVariable("mission").setValue(tempRobotLive.mission_text)
                        guli.GuliVariable("state").setValue(tempRobotLive.state_text)
                    except:
                        pass
                    db.commit()
                print(f'Added {tempRobotLive.robot_name} live data to database')
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting maps - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting maps - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting maps.")
        print("Error not defined.")
    finally:
        getRobotLive.close()

# Getting robot live data from mir_db
def getFromMirDB(db, cursor):
    cursor.execute("USE MIR_DB")
    battery_values = 'SELECT * FROM robots_live_data;'
    cursor.execute(battery_values)
    myresult = cursor.fetchall()
    fields = ['id', 'name', 'battery', 'battery_time_remain', 'uptime', 'state', 'distance', 'errors', 'mission', 'timestamp']
    with open('live_data.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(myresult)

    print(f'Fetched {len(myresult)} rows from database.')

# Getting maps details
class Map:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def getMaps(db, cursor):
    # Getting maps from MIR
    try:
        getMaps = requests.get (ld.MIR_host + "maps", headers = ld.MIR_headers)
        match getMaps.status_code:
            case 200:
                mapsJson = getMaps.json()
                for i in range(len(mapsJson)):
                    tempMap = Map(**mapsJson[i])
                    cursor.execute('USE MIR_DB')
                    map_values = ('INSERT IGNORE INTO maps (name, guid, url, timestamp) '
                                   f'VALUES (\'{tempMap.name}\', \'{tempMap.guid}\', \'{tempMap.url}\','
                                   f'\'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\');')
                    cursor.execute(map_values)
                    db.commit()
                print(f'Added {len(mapsJson)} maps to database.')
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting maps - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting maps - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting maps.")
        print("Error not defined.")
    finally:
        getMaps.close()

# Getting positions details
class Position:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def getPosGUIDS():
# Getting positions guid's from all maps
    try:
        getPositions = requests.get (ld.MIR_host + "/positions", headers = ld.MIR_headers)
        match getPositions.status_code:
            case 200:
                listOfPosGUIDS = []
                positionsJson = getPositions.json()
                for i in positionsJson:
                    listOfPosGUIDS.append(i["guid"])
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting positions - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting positions - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting positions.")
        print("Error not defined.")
    finally:
        getPositions.close()

    return listOfPosGUIDS

def getPosDetails(db, cursor):

    listOfPosGUIDS = getPosGUIDS()

    # Getting details of positions
    cursor.fetchall()
    cursor.execute('TRUNCATE positions')

    listOfPosDetails = []
    for pos in listOfPosGUIDS:
        try:
            getPosDetails = requests.get (ld.MIR_host + "/positions/" + pos, headers = ld.MIR_headers)
            match getPosDetails.status_code:
                case 200:
                    posDetailsJson = getPosDetails.json()
                    tempPosDetails = Position(**posDetailsJson)
                    cursor.execute('USE MIR_DB')
                    pos_values = ('INSERT INTO positions (name, guid, created_by_name, created_by_id,'
                                  'map_id, pos_x, pos_y, orientation, timestamp)'
                                  f'VALUES (\'{tempPosDetails.name}\', \'{tempPosDetails.guid}\','
                                  f'\'{tempPosDetails.created_by_name}\', \'{tempPosDetails.created_by_id}\','
                                  f'\'{tempPosDetails.map_id}\', \'{tempPosDetails.pos_x}\','
                                  f'\'{tempPosDetails.pos_y}\', \'{tempPosDetails.orientation}\','
                                  f'\'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\')'
                                  f'ON DUPLICATE KEY UPDATE guid = \'{tempPosDetails.guid}\';')
                    cursor.execute(pos_values)
                    db.commit()
                case 400:
                    raise ue.Error400
                case 404:
                    raise ue.Error404
                case _:
                    raise ue.ErrorUnknown
        except ue.Error400:
            print("Error with getting position details - code 400.")
            print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
        except ue.Error404:
            print("Error with getting position details - code 404.")
            print("Not found.")
        except ue.ErrorUnknown:
            print("Error with getting position details.")
            print("Error not defined.")
        finally:
            getPosDetails.close()
    print(f'Added {len(listOfPosGUIDS)} points to database.')

# Getting software logs (UPGRADE/RESTORE)
class Software_Log:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def getSoftwareLogs(db, cursor):
    try:
        getLogs = requests.get (ld.MIR_host + 'software/logs' , headers = ld.MIR_headers)
        match getLogs.status_code:
            case 200:
                logsJson = getLogs.json()
                cursor.execute('USE MIR_DB')
                cursor.execute('TRUNCATE software_logs;')
                for i in range(len(logsJson)):
                    tempLogs = Software_Log(**logsJson[i])
                    logs_values = ('INSERT IGNORE INTO software_logs (guid, from_ver, to_ver, state, action, '
                                   'start_time, end_time) '
                                   f'VALUES (\'{tempLogs.guid}\', \'{tempLogs.__dict__["from"]}\','
                                   f'\'{tempLogs.to}\', \'{tempLogs.state}\','
                                   f'\'{tempLogs.action}\', \'{tempLogs.start_time}\','
                                   f'\'{tempLogs.end_time}\');')
                    cursor.execute(logs_values)
                    db.commit()
                print(f"Added {len(logsJson)} software logs to database")
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting software logs - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting software logs - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting software logs.")
        print("Error not defined.")
    finally:
        getLogs.close()

# Getting error logs
class Error_Log:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def getErrorLogsIDS():
    try:
        getErrorLogsID = requests.get (ld.MIR_host + "/log/error_reports", headers = ld.MIR_headers)
        match getErrorLogsID.status_code:
            case 200:
                listOfErrorLogsId = []
                errorLogsJson = getErrorLogsID.json()
                for pos in errorLogsJson:
                    listOfErrorLogsId.append(pos["id"])
            case 400:
                raise ue.Error400
            case 404:
                raise ue.Error404
            case _:
                raise ue.ErrorUnknown
    except ue.Error400:
        print("Error with getting error logs ID's - code 400.")
        print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
    except ue.Error404:
        print("Error with getting error logs ID's - code 404.")
        print("Not found.")
    except ue.ErrorUnknown:
        print("Error with getting error logs ID's.")
        print("Error not defined.")
    finally:
        getErrorLogsID.close()

    return listOfErrorLogsId

def getErrorLogs(db, cursor):

    listOfErrorLogsIDS = getErrorLogsIDS()

    cursor.execute('TRUNCATE error_logs;')
    for pos in listOfErrorLogsIDS:
        try:
            getErrorReports = requests.get (ld.MIR_host + "/log/error_reports/" + str(pos), headers = ld.MIR_headers, verify=False)
            match getErrorReports.status_code:
                case 200:
                    errorReportsJson = getErrorReports.json()
                    tempErrorReport = Error_Log(**errorReportsJson)
                    tempErrorReport.description = tempErrorReport.description.replace("'","")
                    cursor.execute('USE MIR_DB')
                    error_values = ('INSERT INTO error_logs (id, description, module, download_url, time)'
                                  f'VALUES (\'{tempErrorReport.id}\', \'{tempErrorReport.description}\','
                                  f'\'{tempErrorReport.module}\', \'{tempErrorReport.download_url}\','
                                  f'\'{tempErrorReport.time}\');')
                    cursor.execute(error_values)
                    db.commit()
                case 400:
                    raise ue.Error400
                case 404:
                    raise ue.Error404
                case _:
                    raise ue.ErrorUnknown
        except ue.Error400:
            print("Error with getting position details - code 400.")
            print("Invalid ordering or Invalid filters or Wrong output fields or Invalid limits.")
        except ue.Error404:
            print("Error with getting position details - code 404.")
            print("Not found.")
        except ue.ErrorUnknown:
            print("Error with getting position details.")
            print("Error not defined.")
        except requests.exceptions.ConnectionError:
            getErrorReports.status_code = "Connection refused"
        finally:
            getErrorReports.close()
    print(f'Added {len(listOfErrorLogsIDS)} error logs to database.')
