select cost, cost_per_1_mwh, numbers_mwh, number_of_month, ecm.number_of_month as miesiac, ecy.name as rok, ect.name as typ_faktury
from electricity_cost_invoices  eci
left outer join main.electricity_cost_energysuppliers ece on eci.energysuppliers_id = ece.id
left outer join main.electricity_cost_typeofinvoice ect on eci.type_of_invoice_id = ect.id
left outer join main.electricity_cost_month ecm on eci.biling_month_id = ecm.id
left outer join main.electricity_cost_year ecy on eci.biling_year_id = ecy.id
where type_of_invoice_id = 1