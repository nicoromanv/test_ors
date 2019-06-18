import psycopg2
from smart_open import open as s_open
from csv import DictWriter, DictReader

from sources.config import Settings


conn_string = f'host={Settings.USER_DB_HOST} ' \
    f'port={Settings.USER_DB_PORT} ' \
    f'dbname={Settings.USER_DB_DATABASE} ' \
    f'user={Settings.USER_DB_USER} ' \
    f'password={Settings.USER_DB_PASSWORD}'

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

error_records = []

with open('sqls/insert_clients.sql', 'r') as query_file:
    query = query_file.read()

with s_open('s3://orsan-etl/clients-transform.csv', 'r') as input_data:
    reader = DictReader(input_data)

    client_headers = reader.fieldnames

    fieldnames = ['orsan_id', 'pg_id', 'rut']

    with s_open('s3://orsan-etl/clients-dict.csv', 'w') as output_data:
        writer = DictWriter(output_data, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['comuna_id']:
                cursor.execute(
                    query,
                    (
                        row['rut'],
                        row['is_active'],
                        row['is_main'],
                        row['address'],
                        row['comuna_id'],
                        row['phone'],
                        row['first_name'],
                        row['last_name'],
                        row['nombre_fantasia'],
                        row['razon_social'],
                        row['type_id'],
                    )
                )
            else:
                error_records.append(row)
                cursor.execute(
                    query,
                    (
                        row['rut'],
                        row['is_active'],
                        row['is_main'],
                        row['address'] or 'No hay dirección',
                        309,
                        row['phone'],
                        row['first_name'],
                        row['last_name'],
                        row['nombre_fantasia'],
                        row['razon_social'],
                        row['type_id'],
                    )
                )

            pg_id = cursor.fetchone()[0]
            writer.writerow({
                'orsan_id': row['orsan_id'],
                'pg_id': pg_id,
                'rut': row['rut'],
            })

        conn.commit()


with s_open('s3://orsan-etl/client_errors.csv', 'w') as errors_file:
    writer = DictWriter(errors_file, fieldnames=client_headers)
    writer.writeheader()

    for row in error_records:
        writer.writerow(row)



