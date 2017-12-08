### Creating the database

The database source is made with SQLite3. With Python 3, the group created SQL queries and parsed the output into JSON for input into MongoDB. 

1. Download the source database from [the million song database](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/mxm_dataset.db)

2. Run `parseDB.py`. It will output tracks.json, which contains all the tracks with lyrics and genres. Python connects to the SQLite DB, and uses the query:

>SELECT * from (SELECT * FROM tracks t JOIN genres g ON t.track_id=g.track_id) as t1 JOIN (SELECT cur.track_id, cur.word, cur.count FROM lyrics cur WHERE NOT EXISTS( SELECT * FROM lyrics high WHERE high.track_id=cur.track_id and high.count > cur.count)) as t2 ON t2.track_id=t1.track_id

to join 1) the highest count word per song and 2) the songs with valid genres (as some songs don't have genres).

### Creating the Mongo Replication Database

1. Setting up the folder
	Create a directory name replicates
		`mkdir replicates`
	Change the current directory to replicates
		`cd replicates`
	Create three folders inside replicates named server1, server2, and server3
		`mkdir server1`
		`mkdir server2`
		`mkdir server3`
  
2. Running the servers
	Open a new terminal in the replicates folder
		`mongod --replSet replicate --dbpath server1 --port 27020 --rest`
	Open another new terminal in the replicates folder 
		`mongod --replSet replicate --dbpath server2 --port 27021 --rest`
	Open another new terminal in the replicates folder
		`mongod --replSet replicate --dbpath server3 --port 27022 --rest`

3. Login to a mongo instance
	mongo localhost:27020

4. Create a cfg file in the terminal

> 
  var cfg = {
    "_id": "replicate",
    "version" : 1,
    "members" :   [
      {
        "_id" : 0,
        "host" : "localhost:27020",
        "priority" : 1
      },
      {
        "_id" : 1,
        "host" : "localhost:27021",
        "priority" : 0
      },
      {
        "_id" : 2,
        "host" : "localhost:27022",
        "priority" : 0
      }
    ]   } 	rs.initialize(cfg)

  
5. Upload the database into the server
 	Run a new terminal in the folder of the json file to be uploaded. Use the tracks.json generated during the `Creating the Database` section
 		`mongoimport --db <dbname> --collection <collection name> --type json --file <filename.json> -h localhost:27020`

6. Check if the files are uploaded
	Go back to the terminal of the server
  Show the current databases
  	`show dbs`
  Use the uploaded database
  	`use <dbname>`
  Check the collection if the data is uploaded
  	`db.<collection name>.find()`

7. Changing the database
	Open a new terminal and login to another port
		`mongo localhost:27021` 
  Once login set the current terminal as a slave
  	`rs.slave.Ok()`
  Then use the uploaded database
  	`use <dbname>`
	Check the database if the same data is uploaded
		`db.<collection name>.find()`

### Sharding the MapReduce collection

1. Setting up the folders
  	Set-up the project folder.
		`mkdir sharding`
	Change the current directory to sharding
	Create four folders in the mongos diectory
   		`mkdir config`
	   	`mkdir shard1`
	   	`mkdir shard2`
	   	`mkdir mongos`

2. Setting up the servers
	Open a terminal within the the sharding folder.
	Set up the config server
		`mongod --configsvr --replSet shard --dbpath config --port 27020`
	Set up the shards
		Open a terminal and setup shard 1
			`mongod --shardsvr --dbpath shard1 --port 27021`
		Open another terminal and setup shard2
			`mongod --shardsvr --dbpath shard2 --port 27022`

3. Setting up the sharding configuration
	Connect to the config server
		`mongod localhost:27020`
	Initiate the replicate set config
		`rs.initiate()`
		
4. Setting up the mongos server
	Set up the mongos folder
		`mongos --configdb shard/localhost:27020 --port 27023`
	Connect to the mongos server
		`mongo localhost:27023`
	Configure the defaul chunkSize
		`use config`
		`db.settings.save({_id:"chunkSize",value: 1})`
	Add the shards
		`sh.addShard("localhost:27021")`
		`sh.addShard("localhost:27022")`

5. Importing the data to the mongos server
	`mongoimport --db <dbname> --collection <collection name> --type json --file <filename.json> --h localhost:27023`

### Creating and using MapReduce

1. Set-up and login into your mongos server

2. Assuming your mongos server is set up and the data has been imported, open the contents of 'MapReduce.js'

3. Copy the contents into the mongos server terminal. This will create the new reduced collections.

4. To know if the MapReduce worked, the response on mongo should follow the similar convention:


      >{
              "result" : "record.answer4",
              "timeMillis" : 5312,
              "counts" : {
    	              "input" : 189481,
                      "emit" : 189481,
                      "reduce" : 30897,
                      "output" : 23738
              },
              "ok" : 1
      }

5. To use the collections, type `db.nameOfMapReduce.find()` as if you were finding a normal collection.
## Additional Notes

### Making queries for sqlite3

1. Open cmd, and type `python` to open the python shell.

2. Type/paste the following code in, which connects to the db and makes queries:

```import sqlite3
con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
cur.execute("<QUERY HERE>")
cur.fetchall()
```

### Exporting and importing json into mongodb

After running the python programs, the data will be input into mongodb. This data can be output into JSON for sharing with other systems.

1. To output, run in your cmd `mongoexport -d <databasename> -c <collectionname> -o <outputname>.json`. In our case, `mongoexport -d test_db -c songs -o tracksOut.json` and `mongoexport -d test_db -c lyrics -o lyricsOut.json`

2. To input json, run in your cmd `mongoimport --db test_db --collections <collectionname> --type json --file <filename>.json`

3. Don't forget to use CMD in the same folder as the JSON you're importing/exporting
