import streamlit as st
from pages.reports.get_modificate_data import PrepareDataForPivotTable, CompareDataFromUsageAndInvoices

with st.container(border=True):
    st.markdown('Raport z użycie poszczególnych instytucji')

    # pobieram i fitlruje dane na temat odczytow, filtruje tylko po glownych licznikach objektow
    dataForPivotUsage = PrepareDataForPivotTable()
    data_about_usage = dataForPivotUsage.get_data('energy_usage')
    data_to_analyse_usage = dataForPivotUsage.filter_data(data_about_usage)

    # pobieram dane na temat faktur
    dataForPivotInvoices = PrepareDataForPivotTable()
    data_about_invoices = dataForPivotUsage.get_data('energy_invoices')

    # sumuje zuzycie instytucji w miesiacach i latach
    compareDataUsageInvoices = CompareDataFromUsageAndInvoices()
    data_about_usage_group = compareDataUsageInvoices.sum_data_by_company(data_to_analyse_usage)

    #############testy#########
    st.dataframe(data_to_analyse_usage)
    st.dataframe(data_about_invoices)
    st.dataframe(data_about_usage_group)
