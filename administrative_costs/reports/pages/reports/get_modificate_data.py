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

    def filter_data(self, data) -> pd.DataFrame:
        """Funkcja odfiltrowuje jedynie liczniki glownych poszczegolnych stref."""
        # wybrane liczniki, ktore swoim zasiegiem obejmuja wszystkie podmioty

        data_to_return = data.loc[data['id_licznika'].isin(self.id_energy_meters)]
        return data_to_return


class CompareDataFromUsageAndInvoices:
    """Zadaniem klasy jest porownanie danych z odczytow licznikow a nastepnie porownanie ich z danymi z faktur.
    W kolejnym kroku dochodzi do wyliczenia tzw straty i rodzielenia procentowo jej."""

    def __init__(self):
        pass

    @staticmethod
    def sum_data_by_company(data) -> pd.DataFrame:
        """Zadaniem metody jest swtorznie nowego dataframe ktory polaczy wszystkie zuzycia danje instytuacji
        z wielu licznikow w jedna wartosc"""
        uniq_years = data['rok'].drop_duplicates().to_list()
        uniq_months = data['miesiac'].drop_duplicates().to_list()
        columns_to_sum = ['usage_cob', 'usage_institute', 'usage_museum', 'usage_parish', 'usage']

        temp_df_sum = pd.DataFrame()
        for year in uniq_years:
            for month in uniq_months:
                temp_in_for = data[columns_to_sum].loc[(data['miesiac'] == month) & (data['rok'] == year)]
                temp_in_for = temp_in_for.cumsum()
                temp_in_for['rok'] = year
                temp_in_for['miesiac'] = month
                if len(temp_in_for) > 1:
                    temp_df_sum = pd.concat([temp_df_sum, temp_in_for.iloc[[-1]]], ignore_index=True)
        return temp_df_sum
