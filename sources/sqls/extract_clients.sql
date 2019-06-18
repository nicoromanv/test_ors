with persons as (
    select row_number()
                   over (partition by C.idAuxiliar order by Poliza.id) as r,
           C.id,
           C.idAuxiliar,
           C.digitoVerif,
           C.esInactivo,
           C.tel1,
           C.tel2,
           C.tel3,
           C.nombre,
           C.apellido,
           C.cia,
           C.sNombre,
           C.sApellido,
           C.tipoContacto,
           CD.linea1,
           CD.linea2,
           CD.linea3,
           CD.indicaciones,
           CD.casa,
           CD.coloniaId
    from Poliza
         left join PolizaMov PM on Poliza.id = PM.polizaId
         left join Contacto C on Poliza.aseguradoId = C.id
                              or Poliza.contratanteId = C.id
                              or PM.productorId = C.id
         left join ContactoDireccion CD on C.id = CD.contactoId
    where len(Poliza.codVerificacion) > 0
      and PM.movimientoId = 1
      and len(C.idAuxiliar) > 0
) select id,
         idAuxiliar,
         digitoVerif,
         esInactivo,
         tel1,
         tel2,
         tel3,
         nombre,
         apellido,
         cia,
         sNombre,
         sApellido,
         tipoContacto,
         linea1,
         linea2,
         linea3,
         indicaciones,
         casa,
         coloniaId
 from persons where r = 1
