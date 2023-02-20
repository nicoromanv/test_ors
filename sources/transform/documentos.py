from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter, DictReader


def transform_docs():

    endosos = {}

    with s_open('s3://orsan-etl/endosos-dict.csv', 'r') as endosos_file:
        reader = DictReader(endosos_file)

        for row in reader:
            endosos[row['orsan_id']] = row['pg_id']

    with s_open('s3://orsan-etl/docs-endosos.csv', 'r') as in_data:
        reader = DictReader(in_data)
        columns = [
            'external_id',
            'orsan_id',
            'description',
            'format',
            'verification_code',
            'file',
        ]

        with s_open('s3://orsan-etl/docs-endosos-transform.csv', 'w') as out_data:
            writer = DictWriter(out_data, fieldnames=columns)
            writer.writeheader()

            for row in tqdm(reader):
                writer.writerow({
                    'external_id': endosos.get(row['endoso_id'], None),
                    'orsan_id': row['doc_id'],
                    'description': row['descripcion'],
                    'format': row['formato'],
                    'verification_code': row['codeVerificacionPoliza'],
                    'file': row['file'],
                })
