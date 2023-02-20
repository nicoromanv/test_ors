insert into poliza_garantia
    (afianzado_id,
     glosa,
     emitido,
     base_id,
     emision,
     has_endoso,
     is_canceled,
     estado)
values (%s, %s, %s, %s, %s, %s, %s, %s)
on conflict (base_id) do update set glosa = excluded.glosa
returning id
