select ecm.name                as licnzik,
       ecm2.meter_reading,
       ecmonth.number_of_month as miesiac,
       ecy.name as rok,
       ecc.usage,
       ecc.usage_cob,
       ecc.usage_institute,
       ecc.usage_museum,
       ecc.usage_parish,
       is_virtual,
       is_add_manual,
       ecm.id as id_licznika
from electricity_cost_energymeters ecm
         left join electricity_cost_meterreadingslist ecml
         left outer join electricity_cost_meterreading ecm2
                         on ecm.id = ecm2.energy_meter_id and ecm2.reading_name_id = ecml.id
         left outer join electricity_cost_month ecmonth
                         on ecml.biling_month_id = ecmonth.id
         left outer join electricity_cost_counterusage ecc
                         on ecm.id = ecc.energy_meter_id and ecml.id = ecc.reading_name_id
left outer join electricity_cost_year ecy
on ecml.biling_year_id = ecy.id
order by ecm.name, miesiac
