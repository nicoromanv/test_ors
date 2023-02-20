from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter, DictReader


def load_endosos(conn):
    cursor = conn.cursor()

    with open('sqls/insert_endosos.sql', 'r') as query_file:
        query = query_file.read()

    with s_open('s3://orsan-etl/endosos-transform.csv', 'r') as input_data:
        reader = DictReader(input_data)

        fieldnames = ['orsan_id', 'pg_id']

        with s_open('s3://orsan-etl/endosos-dict.csv', 'w') as output_data:
            writer = DictWriter(output_data, fieldnames=fieldnames)
            writer.writeheader()

            for row in tqdm(reader):
                cursor.execute(
                    query,
                    (
                        row['emision'] or row['creacion_ts'],
                        row['secuencia_endoso'],
                        row['inicio_vigencia'],
                        row['termino_vigencia'],
                        row['cambio_cobertura_amt'],
                        row['cambio_prima_neta_amt'],
                        row['cambio_iva_amt'],
                        row['cambio_prima_total_amt'],
                        row['cambio_comision_pct'],
                        row['cambio_prima_exenta_neta'],
                        row['emitido'],
                        row['glosa_endoso'],
                        row['glosa'],
                        row['creacion_ts'],
                        row['actualizacion_ts'] or row['creacion_ts'],
                        row['poliza_base_id'],
                        row['tipo_endoso_id'],
                        row['poliza_base_id'],
                    )
                )

                pg_id = cursor.fetchone()[0]
                writer.writerow({
                    'orsan_id': row['orsan_id'],
                    'pg_id': pg_id,
                })

            conn.commit()
