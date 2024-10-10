import streamlit as st
import graphviz
import os
import pandas as pd
from connections.connect_to_databse import connect_to_databse

with st.container(border=True):
    st.markdown('Wykres topologi sieci elektrycznej kompleksu Świątynnego')
    # lacze sie z baza danych i pobieram dane
    conn = connect_to_databse()
    cursor = conn.cursor()
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../sql_queries/energy_meters_tree.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    data = pd.read_sql_query(zapytanie, conn)

    # tworze graf
    graph = graphviz.Digraph()
    # graph.attr(rankdir='LR')
    # graph.attr(margin='0')
      # Rozmiar 10x7 cali; znak "!" wymusza dokładny rozmiar
    # graph.graph_attr['dpi'] = '100'
    # graph.attr(ratio='fill')

    for i, j in data.iterrows():
        graph.edge(str(j['licznik_main']), str(j['licznik_submain']))
        if j['is_virtual']:
            graph.node(str(j['licznik_main']), style='filled', fillcolor='yellow')
    with st.expander('Wykres'):
        st.markdown(
            '''Kolorem żółtym są zaznaczone liczniki tzw. wirtualne tzn. takie które nie występją w rzeczywistości ale 
            są niezbędne do prawidlowego liczenia raportów, oraz lepszego zrozuminia topologi sieci.''')
        graph.attr(rankdir='LR', dpi='80', ratio='fill', margins='0', pad='0.5', splines='True')
        st.graphviz_chart(graph)

    with st.expander('Tabela z danymi'):
        st.dataframe(data)

with st.container(border=True):
    st.markdown('Sprawdzenie czy wszystkie liczniki są przypisane do drzewa liczników')
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../sql_queries/energy_meters_not_included_in_tree.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    data = pd.read_sql_query(zapytanie, conn)
    if len(data) > 0:
        with st.expander('Tabela z licznikami nie przypisanymi do drzewa liczników'):
            st.dataframe(data, use_container_width=True)
    else:
        st.markdown('Wszystkie liczniki znajdują sie w strukturze drzewa')
