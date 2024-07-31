select main.name as licznik_main, submain.name as licznik_submain from electricity_cost_energymetertree tree
left outer join electricity_cost_energymeters main
on tree.energy_meter_main_id = main.id
left outer join electricity_cost_energymeters submain
on tree.energy_meter_submain_id = submain.id