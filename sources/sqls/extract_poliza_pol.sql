select P.registro
from Poliza
left join PolizaMov PM on Poliza.id = PM.polizaId
left join Producto P on Poliza.productoId = P.id
left join PolizaMovObs PMO on PM.id = PMO.polizaMovId
left join Contacto C on PM.productorId = C.id
where PM.movimientoId = 1
  and len(Poliza.codVerificacion) > 0
  and Poliza.sisRamoId <> 7
