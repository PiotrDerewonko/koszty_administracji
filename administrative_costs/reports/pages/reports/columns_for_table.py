import pandas as pd
import locale

# Ustawienie lokalizacji na polski
locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')


class AddColumnsToTable:

    def __init__(self, final_table: pd.DataFrame, temporary_table: pd.DataFrame, company: str, company_to_table: str):
        self.final_table = final_table
        self.temporary_table = temporary_table
        self.company = company
        self.company_to_table = company_to_table
        if len(self.temporary_table.loc[(self.temporary_table['stawka_vat_za energie']) != (
                self.temporary_table['stawka_vat_za przesył'])]) > 0:
            self.one_vat_rate = False
        else:
            self.one_vat_rate = True

    def add_invoice_for_energy(self, description):
        tmp_text = 'Wartość faktury za energię [A]'
        self.final_table[f'{tmp_text}'] = (
                self.temporary_table['cost_za energie'] / (
                1 + (self.temporary_table['stawka_vat_za energie'] / 100))).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        description = description + f'''<b>{tmp_text}</b> - Wysokość netto faktury za energię elektryczną 
        dla kompleksu COB za miesiąc obrachunkowy<br>'''
        return self.final_table, description

    def add_invoice_for_distribution_energy(self, description):
        tmp_text = 'Wartość faktury za przesył [B]'
        self.final_table[f'{tmp_text}'] = (self.temporary_table['cost_za przesył'] / (
                1 + (self.temporary_table['stawka_vat_za przesył'] / 100))).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        description = description + f'''<b>{tmp_text}</b> - Wysokość netto faktury za przesył energii elektrycznej 
        dla kompleksu COB za miesiąc obrachunkowy<br>'''
        return self.final_table, description

    def add_value_of_usage_energy_for_comapny(self):
        self.final_table[f'''Wartość energii elektrycznej<br>
        zużytej przez {self.company_to_table}<br>
        po odczycie z <br>liczników {self.company_to_table}
        za miesiąc<br>obrachunkowy [D]'''] = (
                (self.temporary_table[f'usage_{self.company}'] + self.temporary_table[
                    f'difference_for_{self.company}']) * self.temporary_table[
                    'cost_per_1_kwh_za energie']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table

    def add_value_of_difference_for_company(self, description):
        tmp_text = f'''Wykość straty dla {self.company_to_table} [I]'''
        self.final_table[f'{tmp_text}'] = (
            self.temporary_table[f'difference_for_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość straty przypisanej do {self.company_to_table}, na podstawie 
        udziału. Sposób liczenia (H * F).<br>'''
        return self.final_table, description

    def add_percent_of_usage_energy_for_company(self, description):
        tmp_text = f'''Udział procentowy {self.company_to_table} w zużyciu całego kompleksu [H]'''
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table[f'%_of_usage_for_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} %")
        description = description + f'''<b>{tmp_text}</b> - Udział zużycia {self.company_to_table} w całościowym zużyciu
         kompleksu wedlug liczników. Sposób liczenia (G / D).<br>'''
        return self.final_table, description

    def add_difference(self, description):
        tmp_text = 'Wysokość straty [F]'
        self.final_table[
            f'''{tmp_text}'''] = (self.temporary_table[f'difference']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wysokość straty energi. Sposób wyliczenia (E -D).<br>'''
        return self.final_table, description

    def usage_energy_for_company(self, description):
        tmp_text = f'''Zużycie energii dla {self.company_to_table} [G]'''
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table[f'usage_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Ilość energi zużytej przez {self.company_to_table} według odczytów 
        liczników.<br>'''
        return self.final_table, description

    def add_value_of_cost_per_1_kwh(self, description):
        tmp_text = f'Koszt netto za 1 kw/h dla {self.company_to_table} [C]'
        self.final_table[f'{tmp_text}'] = (
                self.temporary_table['cost_per_1_kwh_za energie'] + self.temporary_table[
            'cost_per_1_kwh_za przesył']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.4f', x, grouping=True)} zł")
        description = description + f'''<b>{tmp_text}</b> - Wysokość netto kosztu za 1 kwh. Koszt ten uwzględnia zarówno
        koszt faktury za energię jak również dystrubucję. Sposób wyliczenia (A / E) + (B / E).<br>'''

        # dodaje dodatkowe kolumny jesli stawki vat roznia sie dla energi i przesylu
        if self.one_vat_rate is False:
            self.final_table['Koszt netto za 1 kw/h energii [C]'] = self.temporary_table[
                'cost_per_1_kwh_za energie'].fillna(0).apply(
                lambda x: f"{locale.format_string('%.4f', x, grouping=True)} zł")
            self.final_table['Koszt netto za 1 kw/h dystrybucji [C]'] = self.temporary_table[
                'cost_per_1_kwh_za przesył'].fillna(0).apply(
                lambda x: f"{locale.format_string('%.4f', x, grouping=True)} zł")
        return self.final_table, description

    def total_cost_for_company(self, description):
        tmp_text = f'Łączny koszt dla {self.company_to_table} [K]'
        self.final_table[f'{tmp_text}'] = (
                (self.temporary_table[f'usage_{self.company}'] * self.temporary_table[
                    'cost_per_1_kwh_za energie']) + (
                        self.temporary_table[f'usage_{self.company}'] * self.temporary_table[
                    'cost_per_1_kwh_za przesył']) + (
                        self.temporary_table[f'cost_per_1_kwh_za energie'] * self.temporary_table[
                    f'difference_for_{self.company}']) + (
                        self.temporary_table[f'cost_per_1_kwh_za przesył'] * self.temporary_table[
                    f'difference_for_{self.company}'])).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        description = description + f'''<b>{tmp_text}</b> - Łączny koszt dla {self.company_to_table}. Sposób liczenia 
        (C * J). <br>'''
        return self.final_table, description

    def add_total_usege_from_meter_readings(self, description):
        tmp_text = 'Zużycie energii kompleksu wg liczników [D]'
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table['numbers_kwh_from_meter_readings']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużycia kompleksu COB, 
        według odczytów z liczników<br>'''
        return self.final_table, description

    def add_total_usege_from_invoices(self, description):
        tmp_text = 'Zużycie energii kompleksu wg operatora [E]'
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table['numbers_kwh_from_invoices']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużycia kompleksu COB, 
        według odczytów operatora.<br>'''
        return self.final_table, description

    def add_total_usage_energy_with_diffrenace(self, description):
        tmp_text = f'Łączne zużycie energii dla {self.company_to_table} [J]'
        self.final_table[
            f'''{tmp_text}'''] = (
                self.temporary_table[f'usage_{self.company}'] +
                self.temporary_table[f'difference_for_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużytej energii przez {self.company_to_table}, 
        według odczytów z liczników oraz wyliczonej straty. Sposób liczenia (G + I).<br>'''
        return self.final_table, description

    def add_vat_rate(self):
        tmp_text = 'Stawki VAT'
        self.final_table['stawka_vat_za energie'] = self.temporary_table['stawka_vat_za energie'].astype(int).astype(str)
        self.final_table['stawka_vat_za przesył'] = self.temporary_table['stawka_vat_za przesył'].astype(int).astype(str)
        if self.one_vat_rate is False:
            self.final_table[f'{tmp_text}'] = (f'''Vat za energię: ''' + self.final_table['stawka_vat_za energie']
                                               + '''%<br> Vat za przesył: ''' +
                                               self.final_table['stawka_vat_za przesył'] + '%')
        else:
            self.final_table[f'{tmp_text}'] = f'VAT {self.final_table["stawka_vat_za energie"].values[0]} %'
        self.final_table = self.final_table.drop(columns=['stawka_vat_za energie', 'stawka_vat_za przesył'])
        return self.final_table

class AddColumnsForTableTelecom(AddColumnsToTable):
    def __init__(self, final_table: pd.DataFrame, temporary_table: pd.DataFrame, company: str, company_to_table: str):
        self.final_table = final_table
        self.temporary_table = temporary_table
        self.company = company
        self.company_to_table = company_to_table

    def add_total_usege_from_meter_readings(self, description):
        tmp_text = 'Zużycie energii kompleksu wg liczników [A]'
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table['energia_kompleks']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużycia kompleksu COB, 
        według odczytów z liczników<br>'''
        return self.final_table, description

    def add_usage_telecom(self, description):
        tmp_text = f'Zużycie energii {self.company_to_table} [B]'
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table[f'usage_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} kwh")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużycia {self.company_to_table}<br>, 
        według odczytów z licznika<br>'''
        return self.final_table, description

    def add_vat(self, description):
        tmp_text = f'Stawki VAT [C]'
        self.final_table[
            f'''{tmp_text}'''] = (
            self.temporary_table[f'usage_{self.company}']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)}")
        description = description + f'''<b>{tmp_text}</b> - Wartość zużycia {self.company_to_table}<br>, 
        według odczytów z licznika<br>'''
        return self.final_table, description


