# Seet
What to achieve in the raspberry Pi

- [ ] Pi connected to NYU wifi
- [x] Pi headless using ssh
- [x] Server connected to AWS server
- [ ] Raw 802.11 data packages sniffing
- [ ] Analysising data packages
- [ ] ensure monitor card not conflict with server card

## Pi connected to NYU wifi

it seems need some kind of NYU sandbox. This part may require IT access

## Pi headless using ssh

### requirement
Ethernet cable <br>
Laptop connect to Wifi

### connection code

```
mac$ ping raspberrypi.local
```
get ip address of RPI
```
mac$ nmap ip
```
making sure it is the pi ip <br>
usually is 169.254.102.169

```
mac$ ssh -v pi@ip
```
password : ipsh


## Server connect to AWS server

### API:
```
import json
import requests

def postData(data):
    api_url = 'http://howfull.us-west-2.elasticbeanstalk.com/postdata'
    create_row_data = {'id': str(data) }
    print(create_row_data)
    r = requests.post(url=api_url, json=create_row_data)
    print(r.status_code, r.reason, r.text)
```
### how to:

```
import postScript as pS

for i in range(1,1000000):
    pS.postData([i,i+1])
```

## Raw 802.11 data packages sniffing Testing
### Aircrack-ng：
Document: <br> 
https://www.aircrack-ng.org/documentation.html <br>
#### start monitor mode

```
pi@raspberrypi:~/Documents/capture $ ifconfig
```
this will give the network card <br>
wlan0 stands for build in wifi card <br>
wlan1 stands for outside wifi card <br>
wlan1 is using for monitor mode, and wlan0 is using for server sending data <br>

Doc for Airmon-ng: <br>
https://www.aircrack-ng.org/doku.php?id=airmon-ng<br>

Check and kill
```
pi@raspberrypi:~/Documents/capture $ sudo airmon-ng check kill
```
Start monitor mode on wlan1 card
```
pi@raspberrypi:~/Documents/capture $ sudo airmon-ng start wlan1
```
now wlan1mon is the monitor mode card

#### Start capturing raw 802.11 frames
Doc for Airodump-ng: <br>
https://www.aircrack-ng.org/doku.php?id=airodump-ng

start monitor in wlan1mon card

```
sudo airodump-ng wlan1mon
```
this will give list of AP info

```
 BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
 44:48:C1:AC:29:63  -66        0        4    1   6  -1   OPN              <length:  0> 
 44:48:C1:AE:C3:C3   -1        0        0    0  11  -1                    CMU-SECURE
 44:48:C1:AF:2E:83  -53       15       16    0   6   54  WPA2 CCMP   MGT  CMU-SECURE 
 44:48:C1:AE:C5:C3  -61        7       47    1   6   54  WPA2 CCMP   MGT  CMU-SECURE
```
Somehow we need to write this info to a file so we can analysis it

```
sudo airodump-ng -w wide --output-format csv --write-interval 3 wlan1mon
```
-w : filename <br>
--output-format: pcap, ivs, csv, gps, kismet, netxml, logcsv <br>
--write-interval: Output file(s) write interval in seconds <br>

now we need to using a scrip to find target AP mac <br>
Then using filter to achieve capture all the data transaction from this AP <br>
For example: 44:48:C1:AE:C5:C3

```
sudo airodump-ng -w target --output-format csv --write-interval 3 --bssid 44:48:C1:AE:C5:C3 wlan1mon
```
now the out come is not very good as:

```
BSSID, First time seen, Last time seen, channel, Speed, Privacy, Cipher, Authentication, Power, # beacons, # IV, LAN IP, ID-length, ESSID, Key
44:48:C1:AE:C5:C3, 2020-02-15 22:11:08, 2020-02-15 22:11:18,  6,  -1, , ,   ,  -1,        0,        0,   0.  0.  0.  0,   0, , 

Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs
AC:88:FD:11:86:7D, 2020-02-15 22:11:08, 2020-02-15 22:11:18, -60,        7, 44:48:C1:AE:C5:C3,
```
even wait for few minutes, the capute clearly not increase <br>
Change a way: now using essid instead of bssid
```
sudo airodump-ng -w target_group --output-format csv --write-interval 3 --essid CMU-SECURE wlan1mon
```
output as:

```
BSSID, First time seen, Last time seen, channel, Speed, Privacy, Cipher, Authentication, Power, # beacons, # IV, LAN IP, ID-length, ESSID, Key
44:48:C1:AF:29:83, 2020-02-15 22:19:32, 2020-02-15 22:19:32, 11,  54, WPA2, CCMP, MGT, -62,        1,        0,   0.  0.  0.  0,  10, CMU-SECURE, 
44:48:C1:AC:2B:63, 2020-02-15 22:19:21, 2020-02-15 22:20:23, 11,  54, WPA2, CCMP, MGT, -64,        1,        0,   0.  0.  0.  0,  10, CMU-SECURE, 
44:48:C1:AE:D4:43, 2020-02-15 22:19:22, 2020-02-15 22:20:16,  6,  54, WPA2, CCMP, MGT, -58,       14,        0,   0.  0.  0.  0,  10, CMU-SECURE, 
44:48:C1:AE:E3:03, 2020-02-15 22:19:18, 2020-02-15 22:20:23, 11,  54, WPA2, CCMP, MGT, -56,       26,        0,   0.  0.  0.  0,  10, CMU-SECURE, 
44:48:C1:AF:2E:83, 2020-02-15 22:19:15, 2020-02-15 22:20:23,  6,  54, WPA2, CCMP, MGT, -58,       27,        2,   0.  0.  0.  0,  10, CMU-SECURE, 

Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs
94:B0:1F:1F:09:73, 2020-02-15 22:20:15, 2020-02-15 22:20:15, -60,        2, (not associated) ,CMU-SECURE
00:5B:94:16:A7:39, 2020-02-15 22:19:29, 2020-02-15 22:20:09, -60,       12, 44:48:C1:AC:29:63,CMU-SECURE
98:01:A7:6C:DE:93, 2020-02-15 22:19:15, 2020-02-15 22:19:37, -60,        6, 44:48:C1:AE:BA:F3,CMU-SECURE
D2:48:51:8A:2C:3D, 2020-02-15 22:19:51, 2020-02-15 22:19:51, -60,        1, (not associated) ,
E0:33:8E:B9:82:E2, 2020-02-15 22:20:01, 2020-02-15 22:20:01, -60,        1, (not associated) ,CMU-SECURE
40:BD:32:77:D1:C9, 2020-02-15 22:19:17, 2020-02-15 22:20:07, -60,       15, (not associated) ,DobilWC
```
this result maybe useful since this command only response for one area. <br>
#### Problem:

1. Floor problem. In CMU, it is very open area that may connect to lower floor AP.
2. Connection problem: the result of this file is unconnected devices right? we need to caculate both attempted and connected devices. But now it seems only capture the attempted devices


### Kismet
#### Summary
Kismet is tool for deep analysis the packages stream <br>
It has user interface, where we can see the number of devices connected to one target AP <br>
But inorder to integrate it with our app and automatize i, we need to scrpited it <br>
#### Kismet database
kimset will generate a file called something.kismet.<br>
this is the file where all the log have been record. <br>
It is sqlite3 database file <br>
https://www.kismetwireless.net/docs/readme/logging/ <br>

after open the database file, we can analysis it <br>

tables:
```
KISMET       data         devices      packets    
alerts       datasources  messages     snapshots
```

Get one line info for devices: 
```
sqlite> .table
sqlite> SELECT ROWID FROM devices;
sqlite> SELECT * FROM devices WHERE ROWID=18363;
// outcome: 
first_time|last_time |devkey                           |phyname   |devmac           |strongest_signal|min_lat|min_lon|max_lat|max_lon|avg_lat|avg_lon|bytes_data |type        |device
1583354652|1583354652|4202770D00000000_636E2EBCFBFE0000|IEEE802.11|FE:FB:BC:2E:6E:63|-76             |0.0    |0.0    |0.0    |0.0    |0.0    |0.0    |0          |Wi-Fi Client|{see file}
```

Get one line info for packets: 
```
sqlite> SELECT ROWID FROM packets;
sqlite> SELECT * FROM packets WHERE ROWID=15;
// outcome:
ts_sec    |ts_usec|phyname   |sourcemac        |destmac          |transmac         |frequency|devkey|lat|lon|alt|speed|heading|packet_len|signal|datasource                          |dlt|packet|error tags
1583352032|755427 |IEEE802.11|88:E9:FE:87:FF:04|00:BE:75:E9:A7:CF|00:00:00:00:00:00|5220000.0|0     |0.0|0.0|0.0|0.0  |0.0    |76        |-62   |A8A60BA1-0000-0000-0000-F018983F8989|127|      |0    |
```

#### Finding number of devices for one ip
finding mac with SSID == "NYU"
### Tshark
### tcpdump
