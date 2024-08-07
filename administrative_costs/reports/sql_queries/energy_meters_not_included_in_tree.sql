select id, name from electricity_cost_energymeters where id not in (
    select energy_meter_submain_id from electricity_cost_energymetertree
    ) and id != 71
