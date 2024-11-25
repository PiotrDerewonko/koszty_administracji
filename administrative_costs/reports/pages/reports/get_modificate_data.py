from connections.connect_to_databse import connect_to_databse
import os
import pandas as pd


class PrepareDataForPivotTable:
    """Zadaniem klasy jest przetowrzenie przekazanych danych na postac tabeli przestawnej. Zalozone czynnosci to
    pobranie danych, ich odfiltorwanie, transpozycja, utworzenie tabeli przestwne, polczenia z kosztami oraz wyliczenie
    straty."""

    id_energy_meters = [70, 72, 73, 74, 75]

    @staticmethod
    def get_data(file):
        """Metoda pobiera dane z zapisanej wczesniej kwerendy."""
        conn = connect_to_databse()
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         f'../../sql_queries/{file}.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()

        data = pd.read_sql_query(zapytanie, conn)
        return data

    def filter_main_energy_meters(self, data) -> pd.DataFrame:
        """Funkcja odfiltrowuje jedynie liczniki glownych poszczegolnych stref."""
        # wybrane liczniki, ktore swoim zasiegiem obejmuja wszystkie podmioty

        data_to_return = data.loc[data['id_licznika'].isin(self.id_energy_meters)]
        return data_to_return

    @staticmethod
    def filter_data_by_years_and_months(data, years: list, month: list) -> pd.DataFrame:
        """Metoda odfitrowuje dane na podstawie rok i miesiąca wybranych przez użytkownikow."""
        data_to_return = data.loc[(data['number_of_month'] >= month[0]) & (data['number_of_month'] <= month[1])]
        if isinstance(years, int):
            years = [years]
        data_to_return['rok'] = data_to_return['rok'].astype(int)
        data_to_return = data_to_return.loc[data_to_return['rok'].isin(years)]
        data_to_return['rok'] = data_to_return['rok'].astype(str)

        return data_to_return


class CompareDataFromUsageAndInvoices:
    """Zadaniem klasy jest porownanie danych z odczytow licznikow a nastepnie porownanie ich z danymi z faktur.
    W kolejnym kroku dochodzi do wyliczenia tzw straty i rodzielenia procentowo jej."""

    def __init__(self, data_usage, data_invoices):
        self.data_usage = data_usage
        self.data_usage_cumulative = pd.DataFrame()
        self.data_invoices = data_invoices

    def sum_data_by_company(self):
        """Zadaniem metody jest swtorznie nowego dataframe ktory polaczy wszystkie zuzycia danje instytuacji
        z wielu licznikow w jedna wartosc"""
        uniq_years = self.data_usage['rok'].drop_duplicates().to_list()
        uniq_months = self.data_usage['number_of_month'].drop_duplicates().to_list()
        columns_to_sum = ['usage_cob', 'usage_institute', 'usage_museum', 'usage_parish', 'usage']

        for year in uniq_years:
            for month in uniq_months:
                temp_in_for = self.data_usage[columns_to_sum].loc[
                    (self.data_usage['number_of_month'] == month) & (self.data_usage['rok'] == year)]
                temp_in_for = temp_in_for.cumsum()
                temp_in_for['rok'] = year
                temp_in_for['number_of_month'] = month
                if len(temp_in_for) > 1:
                    self.data_usage_cumulative = pd.concat([self.data_usage_cumulative, temp_in_for.iloc[[-1]]],
                                                           ignore_index=True)

    def compare_data_usage_invoices(self) -> pd.DataFrame:
        """zadaniem metody jest porownanie danych z licznika z danymi z faktur. Porownujemy ilosc zuzytych jednostyek
        energii"""
        data_invoices_filtered = self.data_invoices[['numbers_kwh', 'number_of_month', 'rok']].loc[
            self.data_invoices['typ_faktury'] == 'za energie']
        data_all = pd.merge(self.data_usage_cumulative, data_invoices_filtered, how='left',
                            left_on=['rok', 'number_of_month'], right_on=['rok', 'number_of_month'])
        data_all['difference'] = data_all['numbers_kwh'] - (
                data_all['usage_cob'] + data_all['usage_institute'] + data_all['usage_museum'] +
                data_all['usage_parish'])
        data_all['% difference'] = (data_all['difference'] / data_all['usage']) * 100
        return data_all

    @staticmethod
    def extra_calculations(data_all):
        """Metoda oblicza dodatkowe kolumny potrzebne do dalszych raportów, oraz poprawia nazwy na lepiej
        okreslajace zawartosc kolumny"""
        data_all.rename(
            columns={'numbers_kwh': 'numbers_kwh_from_invoices', 'usage': 'numbers_kwh_from_meter_readings'},
            inplace=True)
        data_all['%_of_usage_for_cob'] = (data_all['usage_cob'] / data_all['numbers_kwh_from_meter_readings']) * 100
        data_all['%_of_usage_for_institute'] = (data_all['usage_institute'] / data_all[
            'numbers_kwh_from_meter_readings']) * 100
        data_all['%_of_usage_for_museum'] = (data_all['usage_museum'] / data_all[
            'numbers_kwh_from_meter_readings']) * 100
        data_all['%_of_usage_for_parish'] = (data_all['usage_parish'] / data_all[
            'numbers_kwh_from_meter_readings']) * 100
        data_all['difference_for_cob'] = (data_all['%_of_usage_for_cob'] / 100) * data_all['difference']
        data_all['difference_for_institute'] = (data_all['%_of_usage_for_institute'] / 100) * data_all['difference']
        data_all['difference_for_museum'] = (data_all['%_of_usage_for_museum'] / 100) * data_all['difference']
        data_all['difference_for_parish'] = (data_all['%_of_usage_for_parish'] / 100) * data_all['difference']
        return data_all


class PrepareDataForPivotTableTelecom(PrepareDataForPivotTable):
    id_energy_meters = [84, 86, 83, 85]


class CompareDataFromUsageAndUsageGlobalTelecom(CompareDataFromUsageAndInvoices):
    def sum_data_by_company(self):
        """Zadaniem tej metody stworzenie tabeli przestawnej ktora pokaze ile pradu zuzyli poszczegolni
        operatorzy w roku i miesiącu obrachunkowym"""
        self.data_usage_cumulative = pd.pivot_table(self.data_usage, index=['rok', 'number_of_month'],
                                                    columns=['liczniki'],
                                                    values=['usage'], aggfunc='sum')
        self.data_usage_cumulative.columns = ['_'.join(col).strip() for col in
                                              self.data_usage_cumulative.columns.values]

    def compare_data_usage_invoices(self):
        """Zadanmiem tej metody jest porownanie sumy podlicznikow operator z licznikiem glownym telefonii."""
        if len(self.data_invoices) <= 12:
            data_tmp = self.data_invoices.iloc[:, [3, 11, 2, 5]]
            data_tmp = data_tmp.rename(columns={data_tmp.columns[0]: 'energia_kompleks'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[1]: 'vat'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[2]: 'koszt_1_kwh'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[3]: 'strata'})
        else:
            data_tmp = self.data_invoices.iloc[:, [3, 13, 2, 3, 4, 7]]
            data_tmp = data_tmp.rename(columns={data_tmp.columns[0]: 'energia_kompleks'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[1]: 'vat'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[2]: 'koszt_1_kwh'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[3]: 'koszt_1_kwh_energia'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[4]: 'koszt_1_kwh_dystrybucja'})
            data_tmp = data_tmp.rename(columns={data_tmp.columns[5]: 'strata'})
        data_tmp = data_tmp.replace(r"kwh|%|zł|VAT|\s", "", regex=True)
        for col in data_tmp.columns:
            data_tmp[col] = data_tmp[col].replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')

        self.data_usage_cumulative = self.data_usage_cumulative.reset_index()
        self.data_usage_cumulative = self.data_usage_cumulative.rename(columns={'number_of_month': 'numer miesiąca'})
        self.data_usage_cumulative = self.data_usage_cumulative.set_index(['rok', 'numer miesiąca'])
        data_all = pd.merge(self.data_usage_cumulative, data_tmp, how='left', left_index=True,
                            right_index=True)
        return data_all


