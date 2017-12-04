# Read lyrics from parsedLyrics.json
# Then port into mongo
import json
from pymongo import MongoClient

output = []
try:
	with open('lyricsParsed.json', 'r') as file:
		data = file.read()
		lyrics = json.loads(data)
		for lyric in lyrics:
			output.append(lyric)
except Exception as e:
	print(e)

client = MongoClient('localhost', 27017)
db = client.test_db['lyrics']
for lyric in output:
	db.insert_one(lyric)

