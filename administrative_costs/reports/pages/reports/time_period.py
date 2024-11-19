from connections.connect_to_databse import connect_to_databse
import pandas as pd
def add_time_period(month_to_report, year_to_report) -> str:
    # tworze zakres czasu dla tytulu do wykresu
    sub_title = ''
    if month_to_report[0] == month_to_report[1]:
        sub_title += f'za miesiąc {change_month_to_str(month_to_report[0])}'
    else:
        sub_title += f'za miesiące {change_month_to_str(month_to_report[0])}-{change_month_to_str(month_to_report[1])}'

    if year_to_report[0] == year_to_report[1]:
        sub_title += f' w roku {year_to_report[1]} '
    else:
        sub_title += f' w latach {year_to_report[0]}-{year_to_report[-1]} '
    return sub_title

def change_month_to_str(month):
    conn = connect_to_databse()
    sql = f'''select name from electricity_cost_month where number_of_month = {month}'''
    data = pd.read_sql_query(sql, conn)
    return data['name'].iloc[0]