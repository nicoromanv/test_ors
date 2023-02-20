with polizas as (
    select row_number()
                   over (partition by Poliza.id order by Poliza.id) as r,
           Poliza.id,
           Poliza.codigo,
           Poliza.aseguradoId,
           PM.productorId,
           Poliza.fIngreso,
           Poliza.fActualizacion,
           C.tipoContacto,
           PM.rMoneda,
           P.registro,
           Poliza.sisRamoId,
           P.nombre,
           Poliza.contratanteId,
           PMO.comentario,
           Poliza.esEmitida,
           PM.fEmision
    from Poliza
    left join PolizaMov PM on Poliza.id = PM.polizaId
    left join Producto P on Poliza.productoId = P.id
    left join PolizaMovObs PMO on PM.id = PMO.polizaMovId
    left join Contacto C on PM.productorId = C.id
    where PM.movimientoId = 1
      and len(Poliza.codVerificacion) > 0
      and Poliza.sisRamoId <> 7
      and PMO.esInactiva = 0
) select id,
         codigo,
         aseguradoId,
         productorId,
         tipoContacto,
         fIngreso,
         fActualizacion,
         rMoneda,
         registro,
         sisRamoId,
         nombre,
         contratanteId,
         comentario,
         esEmitida,
         fEmision
from polizas where r = 1
