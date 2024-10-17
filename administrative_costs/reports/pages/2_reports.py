import streamlit as st
from pages.reports.get_modificate_data import PrepareDataForPivotTable, CompareDataFromUsageAndInvoices
from pages.reports.report_for_comapnies import ReportForCompanies

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
    compareDataUsageInvoices = CompareDataFromUsageAndInvoices(data_to_analyse_usage, data_about_invoices)
    compareDataUsageInvoices.sum_data_by_company()
    data_compared = compareDataUsageInvoices.compare_data_usage_invoices()
    data_with_extra_calculations = compareDataUsageInvoices.extra_calculations(data_compared)

    # tworze raport dla instytutu
    institute_report = ReportForCompanies(data_with_extra_calculations, data_about_invoices, 'institute')
    institute_report.choose_data()
    institute_report.add_invoices_for_energy('za energie')
    institute_report.add_invoices_for_energy('za przesył')
    institute_report.create_pivot_table()

    #############testy#########
    st.dataframe(data_to_analyse_usage)
    st.dataframe(data_about_invoices)

    st.dataframe(institute_report.data_filltered)
    st.markdown(institute_report.final_table.to_html(escape=False), unsafe_allow_html=True)
