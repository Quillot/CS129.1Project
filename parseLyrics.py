import json
with open('lyrics.json') as file:
	output = []
	# Read the file
	data = file.read()
	# Load it as JSON
	lyrics = json.loads(data)
	prev_lyric = ""
	index = 0
	# Check for repeats in lyrics track id and count
	try:
		for lyric in lyrics:
			if index == 0:
				prev_lyric = lyric
				index += 1
			# If the lyric is not a repeat, print it
			elif not prev_lyric[0] == lyric[0] and not prev_lyric[2] == lyric[2]:
				lyric_json = {
					"track_id": lyric[0],
					"word": lyric[1],
					"word_count": lyric[2]
				}
				output.append(lyric_json)
			prev_lyric = lyric
			index += 1
	except Exception as e:
		pass
	
with open('lyricsParsed.json', 'a') as file:
	file.write(json.dumps(output))