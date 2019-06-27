from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter, DictReader


def get_cambio_comision(row):
    if float(row['rPrimas']) != 0:
        return round(float(row['comMonto'])*100/float(row['rPrimas']), 2)
    return 0


def get_glosa_endoso(row):
    if row['movimientoId'] != '1':
        return row['comentario']
    return None


def get_glosa(row):
    if row['movimientoId'] == '1':
        return row['comentario']
    return None


def transform_endosos():

    tipo_endoso = {
        '1': 1,  # Emision
        '2': 9,  # Anulacion
        '5': 4,  # Reinstalacion
        '8': 5,  # Aumento Suma
        '9': 5,  # Disminucion Suma
        '12': 2,  # Prorroga
    }


    polizas = {}

    with s_open('s3://orsan-etl/polizas-dict.csv', 'r') as clients_file:
        reader = DictReader(clients_file)

        for row in reader:
            polizas[row['orsan_id']] = row['pg_id']

    with s_open('s3://orsan-etl/endosos.csv', 'r') as in_data:
        reader = DictReader(in_data)
        columns = [
            'orsan_id',
            'emision',
            'secuencia_endoso',
            'inicio_vigencia',
            'termino_vigencia',
            'cambio_cobertura_amt',
            'cambio_prima_neta_amt',
            'cambio_iva_amt',
            'cambio_prima_total_amt',
            'cambio_comision_amt',
            'cambio_comision_pct',
            'cambio_prima_exenta_neta',
            'emitido',
            'glosa_endoso',
            'glosa',
            'creacion_ts',
            'actualizacion_ts',
            'poliza_base_id',
            'tipo_endoso_id'
        ]

        with s_open('s3://orsan-etl/endosos-transform.csv', 'w') as out_data:
            writer = DictWriter(out_data, fieldnames=columns)
            writer.writeheader()

            for row in tqdm(reader):
                writer.writerow({
                    'orsan_id': row['endoso_id'],
                    'emision': row['fEmision'],
                    'secuencia_endoso': int(row['num_endoso']) - 1,
                    'inicio_vigencia': row['rFdesde'],
                    'termino_vigencia': row['rFhasta'],
                    'cambio_cobertura_amt': row['sa'],
                    'cambio_prima_neta_amt': row['rPrimas'],
                    'cambio_iva_amt': row['rImpuesto1'],
                    'cambio_prima_total_amt': row['rTotal'],
                    'cambio_comision_amt': row['comMonto'],
                    'cambio_comision_pct': get_cambio_comision(row),
                    'cambio_prima_exenta_neta': 0,
                    'emitido': True,
                    'glosa_endoso': get_glosa_endoso(row),
                    'glosa': get_glosa(row),
                    'creacion_ts': row['fIngreso'],
                    'actualizacion_ts': row['fEmision'],
                    'poliza_base_id': polizas.get(row['id'], None),
                    'tipo_endoso_id': tipo_endoso.get(row['movimientoId'], None),
                })
