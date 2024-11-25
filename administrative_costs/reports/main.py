import streamlit as st
import sys
import os

# podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania kosztów administracyjnych",
                   page_icon=':bar_chart:',
                   layout='wide')


st.page_link('pages/2_reports.py', label='Raport do refakturowania kosztów energii')
