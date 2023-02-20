update Poliza
set codVerificacion = 'M12E2018G5628905000957'
where codigo = '03-24-000957';

update Poliza
set codVerificacion = 'J5E2018G8817011'
where codigo = '03-24-000286';

with cancelaciones
    (polizaId, codigoEvento, nombreEvento, detalleEvento, refId, usuario, fecha)
as (
    select polizaId,
           2 codigoEvento,
           'CANCELACIÓN' nombreEvento,
           '' detalleEvento,
           id refId,
           emitidoPor usuario,
           fEmision fecha
    from PolizaMov
    where id in (694, 695, 696, 697, 698)
    )
insert into PolizaHis
    (polizaId, codigoEvento, nombreEvento, detalleEvento, refId, usuario, fecha)
select * from cancelaciones;

