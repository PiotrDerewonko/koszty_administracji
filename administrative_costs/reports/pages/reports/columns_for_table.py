import pandas as pd
import locale

# Ustawienie lokalizacji na polski
locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')


class AddColumnsToTable:

    def __init__(self, final_table: pd.DataFrame, temporary_table: pd.DataFrame, company: str):
        self.final_table = final_table
        self.temporary_table = temporary_table
        self.company = company

    def add_invoice_for_energy(self):
        self.final_table['''Wartość netto faktury, <br>
        Energia Elektryczna<br>
        dla kompleksu COB<br>
        za miesiąc obrachunkowy [A]'''] = self.temporary_table['cost_za energie'].fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table

    def add_invoice_for_distribution_energy(self):
        self.final_table['''Wartość netto faktury,<br>
        opłata przesyłowa<br>
        dla kompleksu COB<br>
        za miesiąc obrachunkowy [B]'''] = self.temporary_table['cost_za przesył'].fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table

    def add_value_of_diffrences(self):
        self.final_table['''Wartość netto różnicy<br>między danymi z faktury<br>a odczytami z liczników[C]'''] = \
            (self.temporary_table['difference'] * self.temporary_table['cost_per_1_kwh_za energie']).fillna(0).apply(
                lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table

    def add_value_of_usage_energy_for_comapny(self):
        self.final_table['''Wartość energii elektrycznej<br>
        zużytej przez MJP2iPW<br>
        po odczycie z liczników MJP2iPW<br>
        za miesiąc obrachunkowy [D]'''] = (self.temporary_table[f'usage_{self.company}'] * self.temporary_table[
            'cost_per_1_kwh_za energie']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table

    def add_value_of_delivered_energy(self):
        self.final_table[
            '''Wartość opłaty przesyłowej<br>dla Muzeum według współczynnika<br>w miesiącu obrachunkowym[E]'''] = (
                self.temporary_table[f'usage_{self.company}'] * self.temporary_table[
            'cost_per_1_kwh_za przesył']).fillna(0).apply(
            lambda x: f"{locale.format_string('%.2f', x, grouping=True)} zł")
        return self.final_table
