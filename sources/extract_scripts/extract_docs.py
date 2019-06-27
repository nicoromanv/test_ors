import base64
from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter


def extract_docs(conn):
    cursor = conn.cursor()

    with open('sqls/extract_docs.sql', 'r') as file_query:
        query = file_query.read()

    cursor.execute(query)

    columns = [
        'endoso_id',
        'doc_id',
        'titulo',
        'descripcion',
        'formato',
        'codeVerificacionPoliza',
        'file',
    ]

    with s_open('s3://orsan-etl/docs-endosos.csv', 'w') as data:
        writer = DictWriter(data, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(cursor):
            filename = f's3://orsan-etl/documentos/{row[1]}.{row[6]}'

            with s_open(filename, 'wb') as out_file:
                out_file.write(base64.b64decode(bytes(row[7], 'utf-8')))
            writer.writerow({
                'endoso_id': row[1],
                'doc_id': row[3],
                'titulo': row[4],
                'descripcion': row[5],
                'formato': row[6],
                'codeVerificacionPoliza': row[8],
                'file': filename,
            })
