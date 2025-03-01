import sqlite3

con = sqlite3.connect('items.bd')
cur = con.cursor()

s = '''
CREATE TABLE IF NOT EXISTS items (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT NOT NULL,
commentary TEXT,
rating TEXT,
url_image TEXT NOT NULL
)
'''
cur.execute(s)


con.commit()
con.close()