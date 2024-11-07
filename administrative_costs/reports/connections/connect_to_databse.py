from decouple import config
import sqlalchemy as db

def connect_to_databse():
    database = config('NAME')
    user = config('USER')
    password = config('PASSWORD')
    host= config('HOST')
    port = config('PORT')

    # Tworzenie URI połączenia
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    conn = db.create_engine(connection_string)

    return conn
