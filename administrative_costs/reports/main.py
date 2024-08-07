import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from connections.connect_to_databse import connect_to_databse
import pandas as pd


with st.container(border=True):
    # lacze sie z baza danych i pobieram dane
    conn = connect_to_databse()
    cursor = conn.cursor()
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'sql_queries/energy_meters_tree.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    data = pd.read_sql_query(zapytanie, conn)
    st.dataframe(data)