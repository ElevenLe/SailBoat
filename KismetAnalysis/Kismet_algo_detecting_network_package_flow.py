# For reading the kismet file
import sqlite3
import json
# postScript is used for sending data to the server
import postScript as pS 
# OS to run command
import sys
from datetime import datetime
import time

# lock = createLock()
# handle = True

def openDatabase(databasename):
    conn = sqlite3.connect(databasename)
    return conn

def closeDatabase(db):
    db.close()

# this is a main analysis program
# this function will run infinity until external exit
def analysis(db, AP):
    while True:
        macs_set_list = []
        # set check time
        check_a = datetime.timestamp(datetime.now()) - 1
        time.sleep(60)
        check_b = datetime.timestamp(datetime.now()) - 1
        # detecting how many devices alive now
        devices_number = detectingLiveDevices(db, AP, check_a, check_b, macs_set_list)
        print("devices_number : " + str(devices_number))
        # calculate the population
        population = calculate(devices_number)
        print("population : " + str(population))
        # send the data to the server
        #pS.postData(population)
        print("data send")



# this function will count how many devices between check time
def detectingLiveDevices(db, AP, a,b,macs_set_list):
    # put AP into list 
    APlist = []
    APlist.append(AP)
    # general macs for target APs
    APmacs = getMacBySSID(APlist, "-1000", db)
    # get all unique devices with their macs in this minutes
    devices_mac_set_in_minute = getNumberOfConnectedWithTargetAP(db, APmacs,a,b)
    # merge new macs set into total macs set
    number = compressMacsSet(devices_mac_set_in_minute, macs_set_list,4)
    return number

def compressMacsSet(mac_set, mac_set_list, minutes_compress):
    print(mac_set)
    print(mac_set_list)
    if(len(mac_set_list) == 0):
        mac_set_list.append(mac_set)
        return len(mac_set)
    elif (len(mac_set_list) > 0 & len(mac_set_list)< minutes_compress-1):
        mac_set_list.append(mac_set)
        return (compress(mac_set, mac_set_list))
    else:
        # get compress new set and all other sets
        # keep the list as same length for iteration
        number = compress(mac_set,minutes_compress)
        mac_set_list.pop(0)
        mac_set_list.append(mac_set)
        return number-2

def compress(new_set, mac_set_list):
    # union all set in old list with new set
    for mac_set in mac_set_list:
        new_set = new_set.union(mac_set)
    return len(mac_set)

def getMacBySSID(target_name_list, signal_strenght, db):
    print("running get ssid")
    target_ap_mac = []
    ssid = "kismet.device.base.name"
    macaddr = "kismet.device.base.macaddr"
    assoied_first = "dot11.device"
    assoied_second = "dot11.device.num_associated_clients"
    query = 'SELECT * FROM devices WHERE type = "Wi-Fi AP" AND strongest_signal > ?'
    t = (signal_strenght,)
    db.execute(query, t)
    rows = db.fetchall()
    for row in range(len(rows)):
        line = json.loads(rows[row][14].decode('utf-8'))
        for item in target_name_list:
            if line[ssid] == item:
                target_ap_mac.append(line[macaddr])
    
    return target_ap_mac

def getNumberOfConnectedWithTargetAP(db, macs, time_a, time_b):
    #print("time a :" + str(time_a) + "time b : " + str(time_b))
    query = 'SELECT DISTINCT sourcemac FROM packets WHERE destmac = ? AND ts_sec > ? AND ts_sec < ?'
    macs_list = set()
    for macaddr in macs:
        t = (macaddr, time_a, time_b,)
        number = db.execute(query, t)
        rows = db.fetchall()
        for row in range(len(rows)):
            mac = rows[row][0]
            macs_list.add(mac)
    #print(macs_list)
    return macs_list


def calculate(devices_number):
    return devices_number/2


def main():
    # sys.argv[1] is the user input for the kismet database file
    # sys.argv[2] is the user input for target AP name
    conn = openDatabase(sys.argv[1])
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    print("success connect to database with " + sys.argv[1])
    analysis(db, sys.argv[2])
    



main()