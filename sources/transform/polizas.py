from tqdm import tqdm
from smart_open import open as s_open
from csv import DictWriter, DictReader


def transform_polizas(conn):
    cursor = conn.cursor()

    with open('sqls/extract_tipo_cobertura.sql') as file_query:
        query = file_query.read()

    cursor.execute(query)

    rows = cursor.fetchall()

    tipo_cobertura = [(item[1], item[0]) for item in rows]

    with open('sqls/extract_tipologia_ejecucion.sql') as file_query:
        query = file_query.read()

    cursor.execute(query)

    rows = cursor.fetchall()

    tipologia_ejecucion = [(item[1], item[0]) for item in rows]

    def get_tipo_cobertura(row):
        for item in tipo_cobertura:
            if item[0].lower() in row['nombre'].lower():
                return item[1]
        return 22

    def get_tipologia_ejecucion(row):
        for item in tipologia_ejecucion:
            if item[0].lower() in row['nombre'].lower():
                return item[1]
        return 5

    def get_pol(row):
        return row['registro'].split('|')[0].lower()

    def get_tipo_intermediario(row):
        if row['tipoContacto'] == '1':
            return 3
        elif row['tipoContacto'] == '2':
            return 2
        return 1


    producto = {
        '1': 1,  # Contratos
        '3': 3,  # Inmobiliarias
        '4': 4,  # Aduaneras
        '5': 2,  # Fiel desempeño
        '6': 5,  # Riesgos
        '7': 5,  # Credito
    }

    moneda = {
        '1': 1,  # Pesos
        '2': 3,  # UF
        '3': None,  # UTM
        '4': 2,  # USD
        '5': 4,  # EUR
        '8': None,  # USRT
    }

    clients = {}

    with s_open('s3://orsan-etl/clients-dict.csv', 'r') as clients_file:
        reader = DictReader(clients_file)

        for row in reader:
            clients[row['orsan_id']] = row['pg_id']


    with s_open('s3://orsan-etl/polizas.csv', 'r') as in_data:
        reader = DictReader(in_data)
        columns = [
            'orsan_id',
            'nemotecnico',
            'asegurado_id',
            'intermediario_id',
            'creacion_ts',
            'actualizacion_ts',
            'actividad_economica_id',
            'moneda_asegurada_id',
            'poliza_maestra_pol',
            'tipo_intermediario_id',
            'producto_id',
            'tipo_cobertura_id',
            'tipo_institucion_id',
            'tipologia_ejecucion_id',
            'afianzado_id',
            'glosa',
            'emitido',
            'base_id',
            'emision',
            'has_endoso',
        ]

        with s_open('s3://orsan-etl/polizas-transform.csv', 'w') as out_data:
            writer = DictWriter(out_data, fieldnames=columns)
            writer.writeheader()

            for row in tqdm(reader):
                writer.writerow({
                    'orsan_id': row['id'],
                    'nemotecnico': row['codigo'],
                    'asegurado_id': clients.get(row['aseguradoId'], None),
                    'intermediario_id': clients.get(row['productorId'], None),
                    'creacion_ts': row['fIngreso'],
                    'actualizacion_ts': row['fActualizacion'],
                    'actividad_economica_id': 9,
                    'moneda_asegurada_id': moneda.get(row['rMoneda'],None),
                    'poliza_maestra_pol': get_pol(row),
                    'tipo_intermediario_id': get_tipo_intermediario(row),
                    'producto_id': producto.get(row['sisRamoId'], 5),
                    'tipo_cobertura_id': get_tipo_cobertura(row),
                    'tipo_institucion_id': 3,
                    'tipologia_ejecucion_id': get_tipologia_ejecucion(row),
                    'afianzado_id': clients.get(row['contratanteId'], None),
                    'glosa': row['comentario'],
                    'emitido': row['esEmitida'],
                    'base_id': None,
                    'emision': row['fEmision'],
                    'has_endoso': row['esEmitida'],
                })
