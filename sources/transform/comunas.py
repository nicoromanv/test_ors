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

with open('sqls/extract_comunas.sql') as file_query:
    query = file_query.read()

cursor.execute(query)

rows = cursor.fetchall()

comunas = {item[1]: item[0] for item in rows}

with s_open('s3://orsan-etl/comunas.csv', 'r') as in_data:
    reader = DictReader(in_data)

    columns = ['id', 'name', 'pg_id']

    with s_open('s3://orsan-etl/comunas-transform.csv', 'w') as out_data:
        writer = DictWriter(out_data, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            writer.writerow({
                'id': row['id'],
                'name': row['colonia'],
                'pg_id': comunas.get(row['colonia'], None)
            })
