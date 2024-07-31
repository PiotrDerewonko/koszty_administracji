import streamlit as st
import graphviz
import os
import pandas as pd
from connections.connect_to_databse import connect_to_databse




with st.container():
    st.markdown('Wykres topologi sieci elektrycznej kompleksu Świątynnego')
    #lacze sie z baza danych i pobieram dane
    conn = connect_to_databse('')
    cursor = conn.cursor()
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../sql_queries/energy_meters_tree.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    data = pd.read_sql_query(zapytanie, conn)
    st.dataframe(data)


    #tworze graf
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')

    for i, j in data.iterrows():
        graph.edge(str(j['licznik_main']), str(j['licznik_submain']))
    st.graphviz_chart(graph)
