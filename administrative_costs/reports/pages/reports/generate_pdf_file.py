import asyncio

from playwright.sync_api import sync_playwright

class GeneratePdfFile:

    def __init__(self, table, adnotation, title, filename):
        self.table = table
        self.adnotation = adnotation
        self.title = title
        self.filename = f'./pages/reports/pdf_files/{filename}.pdf'

    def create_pdf(self):
        # Definicja stylów CSS
        css_styles = """
        <style>
            body {
                font-family: 'DejaVu Sans', sans-serif;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
                font-size: 12px;
            }
            .table th {
                background-color: #f2f2f2;
            }
        </style>
        """

        # HTML do wygenerowania PDF
        html_content = f"""
        <html>
            <head>
                {css_styles}
            </head>
            <body>
                <h1>{self.title}</h1>
                {self.table}
                <br>Opis pól:
                {self.adnotation}
            </body>
        </html>
        """

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content)
            page.pdf(path=self.filename, format="A4", landscape=True)  # Orientacja pozioma
            browser.close()
