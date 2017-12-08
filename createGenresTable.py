import sqlite3, csv

con = sqlite3.connect("mxm_dataset.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS genres (track_id text PRIMARY KEY, genre text NOT NULL);") 

with open('genres.csv','r', encoding="utf8") as genres_table:
    dr = csv.DictReader(genres_table, ["track_id", "genre"])
    to_db = [(i['track_id'], i['genre']) for i in dr]

cur.executemany("INSERT INTO genres VALUES (?,?);", to_db)
con.commit()