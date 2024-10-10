select ecm2.name     as miesiac,
       ecy.name      as rok,
       ecc.usage_cob as zuzycie,
       'COB'         as podmiot
from electricity_cost_counterusage ecc
         left outer join electricity_cost_meterreadingslist ecm
                         on ecc.reading_name_id = ecm.id
         left outer join electricity_cost_month ecm2
                         on ecm.biling_month_id = ecm2.id
         left outer join electricity_cost_year ecy
                         on ecm.biling_year_id = ecy.id
where energy_meter_id in (70, 72, 73, 74, 75)
union
select ecm2.name           as miesiac,
       ecy.name            as rok,
       ecc.usage_institute as zuzycie,
       'INSTYTUT'          as podmiot
from electricity_cost_counterusage ecc
         left outer join electricity_cost_meterreadingslist ecm
                         on ecc.reading_name_id = ecm.id
         left outer join electricity_cost_month ecm2
                         on ecm.biling_month_id = ecm2.id
         left outer join electricity_cost_year ecy
                         on ecm.biling_year_id = ecy.id
where energy_meter_id in (70, 72, 73, 74, 75)
union
select ecm2.name        as miesiac,
       ecy.name         as rok,
       ecc.usage_museum as zużycie,
       'MUZEUM'         as podmiot
from electricity_cost_counterusage ecc
         left outer join electricity_cost_meterreadingslist ecm
                         on ecc.reading_name_id = ecm.id
         left outer join electricity_cost_month ecm2
                         on ecm.biling_month_id = ecm2.id
         left outer join electricity_cost_year ecy
                         on ecm.biling_year_id = ecy.id
where energy_meter_id in (70, 72, 73, 74, 75)
union
select ecm2.name        as miesiac,
       ecy.name         as rok,
       ecc.usage_parish as zużycie_parafia,
       'PARAFIA'        as podmiot
from electricity_cost_counterusage ecc
         left outer join electricity_cost_meterreadingslist ecm
                         on ecc.reading_name_id = ecm.id
         left outer join electricity_cost_month ecm2
                         on ecm.biling_month_id = ecm2.id
         left outer join electricity_cost_year ecy
                         on ecm.biling_year_id = ecy.id
where energy_meter_id in (70, 72, 73, 74, 75)