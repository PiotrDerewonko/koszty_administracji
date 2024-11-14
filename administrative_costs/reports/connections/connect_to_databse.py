from decouple import config
import sqlalchemy as db
import streamlit as st

def connect_to_databse():
    database = config('DATABASE')
    user = config('USER')
    password = config('PASSWORD')
    host= config('HOST')
    port = config('PORT')

    # Tworzenie URI połączenia
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    conn = db.create_engine(connection_string)

    return conn
