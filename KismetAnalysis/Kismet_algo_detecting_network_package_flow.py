# For reading the kismet file
import sqlite3
import json
# postScript is used for sending data to the server
import postScript as pS 
# OS to run command
import sys
from datetime import datetime


def openKismet():
    subprocess.run(['kismet'])

def openDatabase(databasename):
    conn = sqlite3.connect(databasename)
    return conn


def closeDatabase(db):
    db.close()


# this is a main analysis program
# this function will run infinity until external exit
def analysis(db, AP):
    if(db == None) return
    init_timestamp = datetime.timestamp(datetime.now())
    try:
        while True:
            # set check time
            check_timestamp = init_timestamp - 2
            timeInterval = []
            timeInterval.append(check_timestamp)
            timeInterval.append(init_timestamp)
            # detecting how many devices alive now
            devices_number = detectingLiveDevices(db, AP, timeInterval)
            # calculate the population
            population = calculate(devices_number)
            # send the data to the server
            pS.postData(population)
            # reset init_time
            init_timestamp = datetime.timestamp(datetime.now())
    except:
        return



# this function will count how many devices between check time
def detectingLiveDevices(db, AP, timeInterval):
    # at this moment, how many devices associated with AP?
    # is all this devices still connected?
    # 5 second later
    # how many devices associated with AP?
    # anyone new?
    # is all alive?
    APlist = []
    APlist.append(AP)
    macs = getMacBySSID(APlist, "-100", db)
    number = getNumberOfConnectedWithTargetAP(macs, timeInterval, db)
    return number


def getMacBySSID(target_name_list, signal_strenght, db):
    target_ap_mac = {}
    ssid = "kismet.device.base.name"
    macaddr = "kismet.device.base.macaddr"
    assoied_first = "dot11.device"
    assoied_second = "dot11.device.num_associated_clients"
    query = 'SELECT * FROM devices WHERE type = "Wi-Fi AP" AND strongest_signal>?'
    t = (signal_strenght,)
    db.execute(query, t)
    rows = db.fetchall()

    for row in range(len(rows)):
        line = json.loads(rows[row][14].decode('utf-8'))
        for item in target_name_list:
            if line[ssid] == item:
                print(line[assoied_first][assoied_second])
                target_ap_mac[line[macaddr]] = (item, line[assoied_first][assoied_second])
            
    return target_ap_mac

def getNumberOfConnectedWithTargetAP(macs, timeInterval ,db):

    query = 'SELECT COUNT(DISTINCT sourcemac) FROM packets WHERE destmac = ? AND ts_sec > ? AND ts_sec < ?'

    number_of_devices = 0
    for macaddr in macs:
        t = (macaddr, timeInterval[0], timeInterval[1])
        number = db.execute(query, t)
        rows = db.fetchone()
        number_of_devices += rows[0]
        print("AP name: " + macs[macaddr] + " AP mac: "+ macaddr + " devices connected: " + str(rows[0]))
    return number_of_devices

def calculate(devices_number):
    return devices_number/2


def main():
    # sys.argv[1] is the user input for the kismet database file
    # sys.argv[2] is the user input for target AP name
    try:
        databaseConn = openDatabase(sys.argv[1])
        print("success connect to database with" + sys.argv[1])
        analysis(databaseConn, sys.argv[2])
    except:
        print("Fail to connect to the databse")

