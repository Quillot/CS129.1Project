import sqlite3, csv
import json
from pymongo import MongoClient

con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
print("Successfully connected to database")
# Get all the tracks that may match genres
# tracks, genres, lyrics
# Year, id, artist, title, id, genre, id, word, how many times, weird thing
# Returns 436436 songs
#cur.execute("SELECT * from tracks JOIN genres ON tracks.track_id=genres.track_id") 
cur.execute("SELECT * from (SELECT * FROM tracks t JOIN genres g ON t.track_id=g.track_id) as t1 JOIN (SELECT cur.track_id, cur.word, cur.count FROM lyrics cur WHERE NOT EXISTS( SELECT * FROM lyrics high WHERE high.track_id=cur.track_id and high.count > cur.count)) as t2 ON t2.track_id=t1.track_id") 


#Get all tracks that match genres and lyrics
#cur.execute("SELECT * from tracks JOIN genres ON tracks.track_id=genres.track_id JOIN lyrics ON tracks.track_id=lyrics.track_id") 

results = cur.fetchall()

data = json.dumps(results)
print("Done fetching all tracks with genres")

# Save tracks to json
tracks = []
count = 0
for track in results:
	# (1922, track_id, band, name, track_id, genre, track_id, word, count)
	track_json = {
		"track_id": track[1],
		"title": track[3],
		"band": track[2],
		"year": track[0],
		"genre": track[5],
		"word": track[7],
		"word_count": track[8]
	}
	tracks.append(track_json)
	print("Appending track ", count)
	count += 1

with open('tracksOut.json', 'a') as file:
	file.write(json.dumps(tracks))

# Connect to mongodb for insertion
client = MongoClient('localhost', 27017)
db = client.test_db['tracks']
for track in tracks:
	db.insert_one(track)
	print('Inserting track')
# for song in all_songs:
# 	db.insert_one(song)
print('Done inserting tracks into mongodb')
con.commit()
