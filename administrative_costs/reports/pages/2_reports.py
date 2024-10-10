import streamlit as st

from connections.connect_to_databse import connect_to_databse

with st.container(border=True):
    st.markdown('Raport z użycie poszczególnych instytucji')
    conn = connect_to_databse()
