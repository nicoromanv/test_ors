insert into base_organization
    (rut, is_active, is_main, address, comuna_id, phone, first_name, last_name, nombre_fantasia, razon_social, type_id)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
on conflict (rut) do update set address = excluded.address
returning id
