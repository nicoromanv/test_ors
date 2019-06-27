with docs as (
    select distinct P.id,
                    PM.id    endoso_id,
                    row_number() over (
                        partition by PM.id order by D.creado desc
                        ) as num_doc,
                    D.id doc_id,
                    D.titulo,
                    D.descripcion,
                    D.formato,
                    D.bin,
                    D.codeVerificacionPoliza
    from PolizaHis
             left join PolizaMov PM on PM.id = PolizaHis.refId
             left join Poliza P on PolizaHis.polizaId = P.id
             left join PolizaMovDoc D on PM.id = D.polizaMovId
    where len(P.codVerificacion) > 0
      and P.sisRamoId <> 7
      and len(D.codeVerificacionPoliza) > 0
      and (len(PM.codEndoso) > 0 or PM.movimientoId in (1, 2, 5))
) select * from docs where num_doc = 1
