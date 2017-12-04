import sqlite3, csv
import json
from pymongo import MongoClient

con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
print("Successfully connected to database")
# Get all the tracks that may match sa lyrics and genres
# tracks, genres, lyrics
# Year, id, artist, title, id, genre, id, word, how many times, weird thing
# Returns 436436 songs
cur.execute("SELECT * from tracks JOIN genres ON tracks.track_id=genres.track_id") 

results = cur.fetchall()

data = json.dumps(results)
print("Done fetching all tracks with genres")
# JSON for holding song with track details and lyrics
# # List for holding all the songs
# all_songs = []
# index = 0
# for song in results:
# 	# Convert sql into json, giving them keys
# 	one_song = {
# 		"track_id": song[1],
# 		"title": song[3],
# 		"band": song[2],
# 		"year": song[0],
# 		"genre": song[5],
# 		"word": song[8],
# 		"word_count": song[9]
# 	}
# 	all_songs.append(one_song)
# 	index += 1

# JSON for song with track details only
tracks = []
count = 0
for track in results:
	# (1922, track_id, band, name, track_id, genre)
	track_json = {
		"track_id": track[1],
		"title": track[3],
		"band": track[2],
		"year": track[0],
		"genre": track[5]
	}
	tracks.append(track_json)
	print("Appending track ", count)
	count += 1


# Get most used word per track
# Returns track_id, word, and word count
# 288k entries
cur.execute("SELECT cur.track_id, cur.word, cur.count FROM lyrics cur WHERE NOT EXISTS( SELECT * FROM lyrics high WHERE high.track_id=cur.track_id and high.count > cur.count)")
#cur.execute("SELECT cur.track_id, cur.word, cur.count FROM lyrics cur LEFT JOIN lyrics high ON high.track_id=cur.track_id AND high.count > cur.count WHERE high.track_id IS NULL")


results = cur.fetchall()
data = json.dumps(results)

print("Done fetching all lyrics")
# JSON for lyrics
count = 0
lyrics = []
for lyric in results:
	lyric_json = {
		"track_id": lyric[0],
		"word": lyric[1],
		"word_count": lyric[2]
	}
	lyrics.append(lyric)
	print('Appended lyrics ', count)
	count += 1

# Output the lists into json files
with open('lyrics.json', 'a') as file:
	file.write(json.dumps(lyrics))

print('Done writing lyrics.json')

with open('tracks.json', 'a') as file:
	file.write(json.dumps(tracks))

print('Done writing tracks.json')

# Connect to mongodb for insertion
client = MongoClient('localhost', 27017)
db = client.test_db['songs']
for track in tracks:
	db.insert_one(track)
	print('Inserting track')
# for song in all_songs:
# 	db.insert_one(song)
print('Done inserting tracks into mongodb')
con.commit()