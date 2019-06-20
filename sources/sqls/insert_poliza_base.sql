insert into poliza_base
    (nemotecnico,
     asegurado_id,
     intermediario_id,
     creacion_ts,
     actualizacion_ts,
     actividad_economica_id,
     moneda_asegurada_id,
     tipo_intermediario_id,
     producto_id,
     tipo_cobertura_id,
     tipo_institucion_id,
     tipologia_ejecucion_id,
     poliza_maestra_id)
select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, id from poliza_maestra where poliza_maestra.nemotecnico = %s
on conflict (nemotecnico) do update set actualizacion_ts = now()::timestamp
returning id
