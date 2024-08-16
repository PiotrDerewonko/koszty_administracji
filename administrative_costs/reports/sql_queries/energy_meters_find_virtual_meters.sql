select ece.id,
       ece.energy_meter_main_id,
       ece.energy_meter_submain_id,
       ece2.name,
       ecm.id,
       ecy.name  as rok,
       ecm2.name as rok,
       ecc.usage as zuzycie_licznika,
       ecc.usage * ecms_i.value as zuzycie_intytutu,
       ecc.usage * ecms_m.value as zuzycie_muzeum,
       ecc.usage * ecms_c.value as zuzycie_cob,
       ecc.usage * ecms_p.value as zuzycie_parafia
from electricity_cost_energymetertree ece
         left outer join electricity_cost_energymeters ece2
                         on ece.energy_meter_submain_id = ece2.id
         left outer join electricity_cost_counterusage ecc
                         on ece2.id = ecc.energy_meter_id
         left outer join electricity_cost_meterreadingslist ecm
                         on ecc.reading_name_id = ecm.id
         left outer join electricity_cost_year ecy
                         on ecm.biling_year_id = ecy.id
         left outer join electricity_cost_month ecm2
                         on ecm.biling_month_id = ecm2.id
         left outer join electricity_cost_metershares ecms_i
                         on ece2.institute_share_id = ecms_i.id
         left outer join electricity_cost_metershares ecms_m
                         on ece2.museum_share_id = ecms_m.id
         left outer join electricity_cost_metershares ecms_c
                         on ece2.cob_share_id = ecms_c.id
         left outer join electricity_cost_metershares ecms_p
                         on ece2.parish_share_id = ecms_p.id
where energy_meter_main_id in (select id from electricity_cost_energymeters where is_virtual = True)
  and energy_meter_main_id = 70