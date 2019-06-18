from smart_open import open as s_open
from csv import DictWriter, DictReader


def get_rut(row):
    return f'{row["idAuxiliar"]}-{row["digitoVerif"]}'


def get_phone(row):
    def clean_phone(number):
        return number.replace('-', '').replace('_', '')

    for field in ('tel1', 'tel2', 'tel3'):
        if row[field] is not None and clean_phone(row[field]):
            return clean_phone(row[field])

    return None


def get_address(row):
    address = f'{row["linea1"]} {row["linea2"]} {row["linea3"]} {row["indicaciones"]} {row["casa"]}'
    return address.strip()


def get_name(row):
    if row["tipoContacto"] == '1':
        return (f'{row["nombre"]} {row["sNombre"]}', f'{row["apellido"]} {row["sApellido"]}')
    return (None, None)


def get_company_name(row):
    if row["tipoContacto"] == '2':
        return row["cia"]
    return None


comunas = {}

with s_open('s3://orsan-etl/comunas-transform.csv', 'r') as comuna_file:
    reader = DictReader(comuna_file)

    for row in reader:
        comunas[row['id']] = row['pg_id']


with s_open('s3://orsan-etl/clients.csv', 'r') as in_data:
    reader = DictReader(in_data)
    columns = [
        'rut',
        'is_active',
        'is_main',
        'uuid',
        'address',
        'comuna_id',
        'phone',
        'first_name',
        'last_name',
        'nombre_fantasia',
        'razon_social',
        'type_id',
        'orsan_id',
    ]

    with s_open('s3://orsan-etl/clients-transform.csv', 'w') as out_data:
        writer = DictWriter(out_data, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            if not row['idAuxiliar']:
                continue
            writer.writerow({
                'rut': get_rut(row),
                'is_active': not eval(row["esInactivo"]),
                'is_main': False,
                'uuid': None,
                'address': get_address(row),
                'comuna_id': comunas.get(row['coloniaId'], None),
                'phone': get_phone(row),
                'first_name': get_name(row)[0],
                'last_name': get_name(row)[1],
                'nombre_fantasia': get_company_name(row),
                'razon_social': get_company_name(row),
                'type_id': row['tipoContacto'],
                'orsan_id': row['id']
            })


