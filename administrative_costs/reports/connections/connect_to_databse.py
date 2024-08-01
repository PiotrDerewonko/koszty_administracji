import sqlite3
import os


def connect_to_databse(db_file= None):
    full_path = os.path.abspath('../../db.sqlite3')
    conn = sqlite3.connect(full_path)
    if not os.path.exists(full_path):
        print(f"Baza danych db.sqlite3 nie istnieje.")
    else:
        print(f"Łączenie z bazą danych: db.sqlite3")
    return conn

