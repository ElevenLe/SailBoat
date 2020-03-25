const openDatabase = (filename) => {
    // import the sqlite3 module
    const sqlite3 = require('sqlite3').verbose()

    // create a Database object

    const db = new sqlite3.Database(filename, sqlite3.OPEN_READONLY, (err) => {
        if(err) {
            return console.error(err.message)
        }
        console.log(`Conneted to the ${filename} sqlite database`)
    })

    return db
}

const closeDatabase = (db) => {
    db.close((err) => {
        if(err){
            return console.error(err.message)
        }
        console.log('Close the database connection')
    })
}

const db = openDatabase('Kismet-20200304-20-00-08-1.kismet')

/* tables:  KISMET       data         devices      packets    
            alerts       datasources  messages     snapshots*/
// Get one line info for devices: 
// SELECT * FROM devices WHERE ROWID=18363;
/*
first_time|last_time |devkey                           |phyname   |devmac           |strongest_signal|min_lat|min_lon|max_lat|max_lon|avg_lat|avg_lon|bytes_data |type        |device
1583354652|1583354652|4202770D00000000_636E2EBCFBFE0000|IEEE802.11|FE:FB:BC:2E:6E:63|-76             |0.0    |0.0    |0.0    |0.0    |0.0    |0.0    |0          |Wi-Fi Client|{see file}
*/

// Get one line info for packets: 
// SELECT ROWID FROM packets
// SELECT * FROM packets WHERE ROWID=15;
/* 
ts_sec    |ts_usec|phyname   |sourcemac        |destmac          |transmac         |frequency|devkey|lat|lon|alt|speed|heading|packet_len|signal|datasource                          |dlt|packet|error tags
1583352032|755427 |IEEE802.11|88:E9:FE:87:FF:04|00:BE:75:E9:A7:CF|00:00:00:00:00:00|5220000.0|0     |0.0|0.0|0.0|0.0  |0.0    |76        |-62   |A8A60BA1-0000-0000-0000-F018983F8989|127|      |0    |
*/
let sql = `SELECT * FROM  `


closeDatabase(db)