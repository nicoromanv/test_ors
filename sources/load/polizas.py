import psycopg2
from smart_open import open as s_open
from csv import DictWriter, DictReader

from sources.config import Settings


conn_string = f'host={Settings.POLIZA_DB_HOST} ' \
    f'port={Settings.POLIZA_DB_PORT} ' \
    f'dbname={Settings.POLIZA_DB_DATABASE} ' \
    f'user={Settings.POLIZA_DB_USER} ' \
    f'password={Settings.POLIZA_DB_PASSWORD}'

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

with open('sqls/insert_poliza_base.sql', 'r') as query_file:
    query_base = query_file.read()

with open('sqls/insert_poliza_garantia.sql', 'r') as query_file:
    query_garantia = query_file.read()

with s_open('s3://orsan-etl/polizas-transform.csv', 'r') as input_data:
    reader = DictReader(input_data)

    fieldnames = ['orsan_id', 'pg_id']

    with s_open('s3://orsan-etl/polizas-dict.csv', 'w') as output_data:
        writer = DictWriter(output_data, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            cursor.execute(
                query_base,
                (
                    row['nemotecnico'],
                    row['asegurado_id'],
                    row['intermediario_id'] or None,
                    row['creacion_ts'],
                    row['actualizacion_ts'] or row['creacion_ts'],
                    row['actividad_economica_id'],
                    row['moneda_asegurada_id'],
                    row['tipo_intermediario_id'],
                    row['producto_id'],
                    row['tipo_cobertura_id'],
                    row['tipo_institucion_id'],
                    row['tipologia_ejecucion_id'],
                    row['poliza_maestra_pol'],
                )
            )

            base_id = cursor.fetchone()[0]

            cursor.execute(
                query_garantia,
                (
                    row['afianzado_id'],
                    row['glosa'],
                    row['emitido'],
                    base_id,
                    row['emision'] or row['creacion_ts'],
                    row['has_endoso'],
                    False,
                    'emitida'
                )
            )

            pg_id = cursor.fetchone()[0]
            writer.writerow({
                'orsan_id': row['orsan_id'],
                'pg_id': pg_id,
            })

            conn.commit()
