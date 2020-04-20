import sqlite3
import json

sqlite_file = "Kismet-20200304-20-00-08-1.kismet"


def openDatabase(databasename):
    conn = sqlite3.connect(databasename)
    return conn


def closeDatabase(db):
    db.close()


def getMacBySSID(target_name, db):
    target_ap_mac = []
    ssid = "kismet.device.base.name"
    macaddr = "kismet.device.base.macaddr"

    db.execute('SELECT * FROM devices WHERE type = "Wi-Fi AP" AND strongest_signal>-10000')
    rows = db.fetchall()

    for row in range(len(rows)):
        line = json.loads(rows[row][14].decode('utf-8'))
        if line[ssid] == target_name:
            target_ap_mac.append({"ssid":target_name, "macaddr":line[macaddr]})
    return target_ap_mac


def main():
    conn = openDatabase(sqlite_file)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    macs = getMacBySSID('nyu', db)
    print(macs)
    print(len(macs))
    closeDatabase(db)


if __name__ == "__main__":
    main()