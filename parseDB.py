import sqlite3, csv
import json
from pymongo import MongoClient

con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
print("Successfully connected to database")
# Get all the tracks that have complete fields, and matching genres and lyric
# tracks, genres, lyrics 
cur.execute("SELECT * from (SELECT * FROM tracks t JOIN genres g ON t.track_id=g.track_id) as t1 JOIN (SELECT cur.track_id, cur.word, cur.count FROM lyrics cur WHERE NOT EXISTS( SELECT * FROM lyrics high WHERE high.track_id=cur.track_id and high.count > cur.count)) as t2 ON t2.track_id=t1.track_id") 

results = cur.fetchall()

data = json.dumps(results)
print("Done fetching all tracks with genres")

# JSON format for songs
tracks = []
count = 0
for track in results:
	# (year, track_id, band, name, track_id, genre)
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

# Write the JSON  
with open('tracks.json', 'a') as file:
	file.write(json.dumps(tracks))

print('Done writing tracks.json')
con.commit()