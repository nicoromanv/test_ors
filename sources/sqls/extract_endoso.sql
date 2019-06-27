select distinct P.id,
       PM.id endoso_id,
       PM.fEmision,
       row_number() over(
           partition by P.id order by PM.fIngreso
           ) as num_endoso,
       PM.corrEndoso,
       PM.rFdesde,
       PM.rFhasta,
       PM.sa,
       PM.rPrimas,
       PM.rImpuesto1,
       PM.rTotal,
       PM.comMonto,
       PMO.comentario,
       PM.fIngreso,
       PM.movimientoId
from PolizaHis
left join PolizaMov PM on PM.id = PolizaHis.refId
left join Poliza P on PolizaHis.polizaId = P.id
left join PolizaMovObs PMO on PM.id = PMO.polizaMovId
where len(P.codVerificacion) > 0
  and P.sisRamoId <> 7
  and PMO.esInactiva = 0
--   and PM.fAnulacion is null
  and (len(PM.codEndoso) > 0 or PM.movimientoId in (1, 2, 5))
