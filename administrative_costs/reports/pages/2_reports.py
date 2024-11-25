import streamlit as st
from pages.reports.get_modificate_data import PrepareDataForPivotTable, CompareDataFromUsageAndInvoices
from pages.reports.report_for_comapnies import ReportForCompanies
from pages.reports.generate_pdf_file import GeneratePdfFile
from datetime import datetime
from pages.reports.time_period import add_time_period
# Reszta logiki aplikacji


with st.container(border=True):
    st.markdown('Raport z użycie poszczególnych instytucji')

    # listy do wybory zakresu dat
    current_year = datetime.now().year
    years_range = list(range(2024, current_year + 2 if current_year == 2024 else current_year + 1))
    month_range = list(map(lambda x: x, range(1, 13)))

    # wskazuje zakres czasu za jaki ma być wygenerowany raport
    year_to_report = st.select_slider(options=years_range, value=(years_range[0], years_range[0]),
                                      label='Wybierz zakres lat do raportu')
    month_to_report = st.select_slider(options=month_range, value=(month_range[0], month_range[-1]),
                                       label='Wybierz zakres miesięcy do raportu')

    #tworze podtytul
    subtitle = add_time_period(month_to_report, year_to_report)

    # pobieram i fitlruje dane na temat odczytow, filtruje tylko po glownych licznikach objektow
    dataForPivotUsage = PrepareDataForPivotTable()
    data_about_usage = dataForPivotUsage.get_data('energy_usage')
    data_to_analyse_usage = dataForPivotUsage.filter_main_energy_meters(data_about_usage)
    data_to_analyse_usage_filterd = dataForPivotUsage.filter_data_by_years_and_months(data_to_analyse_usage, year_to_report,
                                                                                      month_to_report)

    # pobieram dane na temat faktur
    dataForPivotInvoices = PrepareDataForPivotTable()
    data_about_invoices = dataForPivotUsage.get_data('energy_invoices')
    data_about_invoices_filtered = dataForPivotInvoices.filter_data_by_years_and_months(data_about_invoices,
                                                                                        year_to_report, month_to_report)

    # sumuje zuzycie instytucji w miesiacach i latach
    compareDataUsageInvoices = CompareDataFromUsageAndInvoices(data_to_analyse_usage_filterd, data_about_invoices_filtered)
    compareDataUsageInvoices.sum_data_by_company()
    data_compared = compareDataUsageInvoices.compare_data_usage_invoices()
    data_with_extra_calculations = compareDataUsageInvoices.extra_calculations(data_compared)

    # tworze zakładki dla poszczególny
    tab_institute, tab_museum, tab_cob, tab_parich = st.tabs(['Raport kosztów instytutu', 'Raport kosztów Muzeum',
                                                              'Raport kosztów COB', 'Raport kosztów Parafii'])


    def generate_report(tab, data_from_energy_meters, invoices, category, name):
        with tab:
            report = ReportForCompanies(data_from_energy_meters, invoices, category, name)
            report.choose_data()
            report.add_invoices_for_energy('za energie')
            report.add_invoices_for_energy('za przesył')
            report.create_pivot_table()
            table_in_html = report.final_table.to_html(classes='table table-bordered', escape=False)
            st.markdown(table_in_html.replace('<table', '<table style="font-size: 13px;"'), unsafe_allow_html=True)
            st.markdown(report.adnotation, unsafe_allow_html=True)
            pdf_file = GeneratePdfFile(table_in_html, report.adnotation, f'Raport dla {name} {subtitle}', name)
            pdf_file.create_pdf()
            with open(f"./pages/reports/pdf_files/{name}.pdf", "rb") as file:
                btn = st.download_button(
                    label=f"Pobierz raport dla {name}",
                    data=file,
                    file_name=f"Raport dla {name}.pdf",
                    mime="application/pdf",
                )
            return report.final_table


    generate_report(tab_institute, data_with_extra_calculations, data_about_invoices, 'institute', 'IPJP2')
    generate_report(tab_museum, data_with_extra_calculations, data_about_invoices, 'museum', 'MUZEUM JP2')
    report_cob = generate_report(tab_cob, data_with_extra_calculations, data_about_invoices, 'cob', 'COB')
    generate_report(tab_parich, data_with_extra_calculations, data_about_invoices, 'parish', 'PARAFIA')
