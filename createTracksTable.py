import sqlite3, csv

con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tracks (year integer NOT NULL, track_id text PRIMARY KEY, artist text NOT NULL, title text NOT NULL);") 

with open('tracks.csv','r', encoding="utf8") as tracks_table:
    dr = csv.DictReader(tracks_table, ["year", "track_id", "artist", "title"])
    to_db = [(i['year'], i['track_id'], i['artist'], i['title']) for i in dr]

cur.executemany("INSERT INTO tracks VALUES (?,?,?,?);", to_db)
con.commit()