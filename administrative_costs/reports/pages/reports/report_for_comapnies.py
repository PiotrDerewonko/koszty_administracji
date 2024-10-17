import pandas as pd

from pages.reports.columns_for_table import AddColumnsToTable


class ReportForCompanies:
    def __init__(self, data_calculations, data_from_invoices, company):
        self.data_calculations = data_calculations
        self.data_from_invoices = data_from_invoices
        self.company = company
        self.data_filltered = None
        self.final_table = None

    def choose_data(self) -> None:
        """Metoda odfiltowuje jedynie te kolumnym,ktore dotycza danej firmy (przekazanej w init)"""
        choosed_columns = [f'usage_{self.company}', 'numbers_kwh_from_meter_readings', 'rok', 'number_of_month',
                           'numbers_kwh_from_invoices', 'difference', '% difference', f'%_of_usage_for_{self.company}',
                           f'difference_for_{self.company}']
        self.data_filltered = self.data_calculations[choosed_columns]

    def add_invoices_for_energy(self, type_of_invoice) -> None:
        """Metoda dodaje wartosc z faktury za dany typ faktury do danych z zużycia. Przed przystąpieniem do łączenia
        danych, ustawiam rok i numer miesiac jako index w obu df. Po zakończonej operacji, resetuje indeks."""
        data_invoices_tmp = self.data_from_invoices.loc[self.data_from_invoices['typ_faktury'] == type_of_invoice]
        data_invoices_tmp = data_invoices_tmp.drop(columns=['typ_faktury', 'miesiac'])
        self.data_filltered = self.data_filltered.set_index(['rok', 'number_of_month'])
        data_invoices_tmp = data_invoices_tmp.set_index(['rok', 'number_of_month'])

        columns_from_data_invoices_tmp = data_invoices_tmp.columns.tolist()

        for i in columns_from_data_invoices_tmp:
            data_invoices_tmp = data_invoices_tmp.rename(columns={f'{i}': f'{i}_{type_of_invoice}'})
        self.data_filltered = pd.merge(self.data_filltered, data_invoices_tmp, left_index=True, right_index=True,
                                       how='left')
        self.data_filltered = self.data_filltered.reset_index()

    def create_pivot_table(self) -> None:
        """Tworze tabele z danymi. Tabela to po obrobce wizualnej w koeljnym kroku, będzie finalnym raportem"""

        self.final_table = pd.DataFrame()
        self.final_table['rok'] = self.data_filltered['rok']
        self.final_table['numer miesiąca'] = self.data_filltered['number_of_month']

        add_columns_to_table = AddColumnsToTable(self.final_table, self.data_filltered, self.company)

        ############################## wartosc netto faktury za energie###############################
        self.final_table = add_columns_to_table.add_invoice_for_energy()
#
        ############################## wartosc netto faktury za przesyl###############################
        self.final_table = add_columns_to_table.add_invoice_for_distribution_energy()
#
#         ############################## wartosc straty w zl###############################
        self.final_table = add_columns_to_table.add_value_of_diffrences()
#
#         ############################## wartosc zuzytej energi przez firme###############################
        self.final_table = add_columns_to_table.add_value_of_usage_energy_for_comapny()

#         ############################## wartosc oplaty przesylowej dla firmy###############################
        self.final_table = add_columns_to_table.add_value_of_delivered_energy()

        # na sam koniec ustawiam rok i miesiac jako index
        self.final_table = self.final_table.set_index(['rok', 'numer miesiąca'])
