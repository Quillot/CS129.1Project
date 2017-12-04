### Instructions

1. Open your mongodb server, make sure to listen on 27107 (default). 

2. Make a db named `test_db`.

3. Run `getRows.py`. It will output lyrics.json, tracks.json, and write all the tracks to test_db, under the collection `songs`. `Songs` should contain 436436 entries.

4. Run `parseLyrics.py`. It will remove all the duplicate track lyrics from lyrics.json (Although this means that those with duplicates will not be included in the final db). This will output lyricsParsed.json.

5. Run `getLyrics.py` It will open lyricsParsed.json and write it to test_db, under the collection `lyrics`. `Lyrics` should contain 230084 entries.

### Notes

For reference, check importCode.txt. 

### Making queries for sqlite3

1. Open cmd, and type `python` to open the python shell.

2. Type/paste the following code in, which connects to the db and makes queries:

```import sqlite3
con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
cur.execute("<QUERY HERE>")
cur.fetchall()
```

3. Refer to importCode for sample queries

### Exporting and importing json into mongodb

After running the python programs, the data will be input into mongodb. This data can be output into JSON for sharing with other systems.

1. To output, run in your cmd `mongoexport -d <databasename> -c <collectionname> -o <outputname>.json`. In our case, `mongoexport -d test_db -c songs -o tracksOut.json` and `mongoexport -d test_db -c lyrics -o lyricsOut.json`

2. To input json, run in your cmd `mongoimport --db test_db --collections <collectionname> --type json --file <filename>.json`

3. Don't forget to use CMD in the same folder as the JSON you're importing/exporting