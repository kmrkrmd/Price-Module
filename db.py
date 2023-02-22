import sqlite3
conn=sqlite3.connect("price_module.db")

conn.execute("CREATE TABLE prices(id INTEGER PRIMARY KEY AUTOINCREMENT,base_price TEXT,base_distance TEXT,dap TEXT,tmf TEXT,tmf_range TEXT,status TEXT)")
conn.execute("CREATE TABLE bills(id INTEGER PRIMARY KEY AUTOINCREMENT,duration TEXT,distance TEXT,amount TEXT)")
