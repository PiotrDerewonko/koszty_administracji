import sqlite3
import os
import sqlalchemy as db

def connect_to_databse():
    # full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../administrative_costs/db.sqlite3'))
    # conn = sqlite3.connect(full_path)
    # if not os.path.exists(full_path):
    #     print(f"Baza danych db.sqlite3 nie istnieje.")
    # else:
    #     print(f"Łączenie z bazą danych: db.sqlite3")
    # Dane logowania do bazy danych PostgreSQL
    user = "postgres"
    password = "postgres"
    host = "localhost"  # np. 'localhost' dla lokalnego działania
    port = "11265"  # domyślny port PostgreSQL
    database = "administration_costs"

    # Tworzenie URI połączenia
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    conn = db.create_engine(connection_string)

    return conn
