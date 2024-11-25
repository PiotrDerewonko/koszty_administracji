from pages.reports.report_for_comapnies import ReportForCompanies
import pandas as pd


class ReportForTelecom(ReportForCompanies):

    def choose_data(self) -> None:
        self.data_filltered = self.data_calculations

    def create_pivot_table(self) -> None:
        self.final_table = pd.DataFrame()
        self.final_table['rok'] = self.data_filltered['rok']
        self.final_table['numer miesiąca'] = self.data_filltered['numer miesiąca']
