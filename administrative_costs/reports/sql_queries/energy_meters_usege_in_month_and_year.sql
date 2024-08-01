select ece.name as nazwa_licznika, month.name as miesiac, year.name as rok, ecc.usage
from electricity_cost_counterusage ecc
left outer join electricity_cost_meterreadingslist ecml
on ecc.reading_name_id = ecml.id
left outer join electricity_cost_energymeters ece
on ecc.energy_meter_id = ece.id
left outer join electricity_cost_month month
on ecml.biling_month_id = month.id
left outer join electricity_cost_year year
on ecml.biling_year_id = year.id