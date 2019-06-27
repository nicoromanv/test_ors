from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter


def extract(conn, object):
    cursor = conn.cursor()

    with open(f'sqls/extract_{object}.sql', 'r') as file_query:
        query = file_query.read()

    cursor.execute(query)

    columns = [item[0] for item in cursor.description]

    with s_open(f's3://orsan-etl/{object}.csv', 'w') as data:
        writer = DictWriter(data, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(cursor):
            writer.writerow(dict(zip(columns, row)))
