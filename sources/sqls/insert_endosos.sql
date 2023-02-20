insert into poliza_endosogarantia
    (emision,
     secuencia_endoso,
     inicio_vigencia,
     termino_vigencia,
     cambio_cobertura_amt,
     cambio_prima_neta_amt,
     cambio_iva_amt,
     cambio_prima_total_amt,
     cambio_comision_pct,
     cambio_prima_exenta_neta,
     emitido,
     glosa_endoso,
     glosa,
     creacion_ts,
     actualizacion_ts,
     poliza_base_id,
     tipo_endoso_id,
     beneficiario_id)
select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
       asegurado_id
from poliza_base join poliza_garantia on poliza_base.id = poliza_garantia.base_id
where poliza_garantia.id = %s
returning id
