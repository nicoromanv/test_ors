import pyodbc
from smart_open import open as s_open
from csv import DictWriter
from sources.config import Settings

conn_string = f'DSN={Settings.DRIVER};' \
    f'DATABASE={Settings.DATABASE};' \
    f'UID={Settings.USER};' \
    f'PWD={Settings.PASSWORD}'

conn = pyodbc.connect(conn_string)

cursor = conn.cursor()

with open('sqls/extract_poliza_pol.sql', 'r') as file_query:
    query = file_query.read()

cursor.execute(query)

columns = [item[0] for item in cursor.description]

with s_open('s3://orsan-etl/polizas_pol.csv', 'w') as data:
    writer = DictWriter(data, fieldnames=['pol'])
    writer.writeheader()

    for row in cursor:
        writer.writerow({'pol': row[0].split('|')[0]})
