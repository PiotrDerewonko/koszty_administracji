import streamlit as st
from pages.reports.generate_pdf_file import GeneratePdfFile


def generate_pdf(report, company, subtitle) -> None:
    table_in_html = report.final_table.to_html(classes='table table-bordered', escape=False)
    st.markdown(table_in_html.replace('<table', '<table style="font-size: 13px;"'), unsafe_allow_html=True)
    st.markdown(report.adnotation, unsafe_allow_html=True)
    pdf_file = GeneratePdfFile(table_in_html, report.adnotation, f'Raport dla {company} {subtitle}', company)
    pdf_file.create_pdf()
    with open(f"./pages/reports/pdf_files/{company}.pdf", "rb") as file:
        btn = st.download_button(
            label=f"Pobierz raport dla {company}",
            data=file,
            file_name=f"Raport dla {company}.pdf",
            mime="application/pdf",
        )
