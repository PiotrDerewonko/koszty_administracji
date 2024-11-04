select sum(cost)                             as cost,
       (sum(cost) / sum(numbers_mwh)) / 1000 as cost_per_1_kwh,
       sum(numbers_mwh) * 1000               as numbers_kwh,
       vat.name                              as stawka_vat,
       number_of_month                       as number_of_month,
       ecm.name                              as miesiac,
       ecy.name                              as rok,
       ect.name                              as typ_faktury
from electricity_cost_invoices eci
         left outer join main.electricity_cost_energysuppliers ece on eci.energysuppliers_id = ece.id
         left outer join main.electricity_cost_typeofinvoice ect on eci.type_of_invoice_id = ect.id
         left outer join main.electricity_cost_month ecm on eci.biling_month_id = ecm.id
         left outer join main.electricity_cost_year ecy on eci.biling_year_id = ecy.id
         left outer join main.electricity_cost_vatrate vat on eci.vat_rate_id = vat.id
group by number_of_month, ecm.number_of_month, ecy.name, ect.name
