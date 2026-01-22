import sqlite3

conn = sqlite3.connect("../app/users.db")
cursor = conn.cursor()

cursor.execute("SELECT id, nazev, cena, skladem FROM product")
products = cursor.fetchall()

for p in products:
    print(p)

conn.close()
