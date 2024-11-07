SELECT ecm.name                AS liczniki,
       ecm3.meter_reading,
       ecmonth.number_of_month AS number_of_month,
       ecy.name                AS rok,
       ecc.usage,
       ecc.usage_cob,
       ecc.usage_institute,
       ecc.usage_museum,
       ecc.usage_parish,
       is_virtual,
       is_add_manual,
       ecm.id                  AS id_licznika
from electricity_cost_counterusage ecc
         left outer join electricity_cost_meterreadingslist ecml
                         on ecc.reading_name_id = ecml.id
         left outer join electricity_cost_energymeters ecm
                         on ecc.energy_meter_id = ecm.id
         left outer join electricity_cost_meterreading ecm3
                         on ecm.id = ecm3.energy_meter_id
                             and ecml.id = ecm3.reading_name_id
         LEFT JOIN electricity_cost_year ecy
                   ON ecml.biling_year_id = ecy.id
             LEFT JOIN electricity_cost_month ecmonth
                   ON ecml.biling_month_id = ecmonth.id
order by rok, number_of_month
