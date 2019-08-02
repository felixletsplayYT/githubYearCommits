import hashlib
import sqlite3
from version import VERSION
pw = input("Your Backend password: ")
hashed = hashlib.sha256(pw.encode()).hexdigest() + ""
db = sqlite3.connect("database")
db.execute("CREATE TABLE IF NOT EXISTS settings (setting string PRIMARY KEY, value string)")
db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("password", hashed))
db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("cache", "1220"))
db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("allow-force", "true"))
db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("allow-user-unregistered", "true"))
# db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("duration", "year"))
db.execute("INSERT INTO settings (setting, value) VALUES (?, ?)", ("version", str(VERSION - 0.2)))
db.execute("CREATE TABLE IF NOT EXISTS user (username string PRIMARY KEY NOT NULL)")
db.execute("INSERT INTO user (username) VALUES ('strifel')")
db.commit()
db.close()