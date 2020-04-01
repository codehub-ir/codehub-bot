# -*- coding: utf-8 -*-
def param_gen(detail, text, lang):
    return {"title": "Paster-Bot",
              "detail": detail,
              "script": text,
              "language": lang
              }

import datetime
def simple_time_gen():
    return str(datetime.datetime.now().strftime("%Y - %m - %d  %H:%W "))

import sqlite3
def connection_gen():
    return sqlite3.connect("users.db", check_same_thread=False)

def table_gen(c):
    c.execute("""CREATE TABLE IF NOT EXISTS table1 (
        id INTEGER PRIMARY KEY,
        name varchar(1024),
        date varchar(1024)
        )""")
    
def insert__(c, conn, id_, name, date):
    c.execute("SELECT * FROM table1 WHERE id=?", (id_,))
    if len(c.fetchall()) == 0:
        c.execute("INSERT INTO table1(id, name, date) VALUES (?,?,?)", (id_, str(name), str(date)))
    conn.commit()

"""
SQLite3 Preparation
1. make a connection
2. make a cursor
3. make table *
"""
import os
def reset_temp_files():
    try:
        os.remove("temp_file_text.txt")
    except:
        pass
    
    try:
        os.remove("temp_file.py")
    except:
        pass