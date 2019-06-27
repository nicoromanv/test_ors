import argparse
import pyodbc
import psycopg2

from config import Settings
from extract_scripts import extract, extract_docs
from transform import transform_clients, transform_polizas, transform_endosos, transform_docs
from load import load_clients, load_polizas, load_endosos


def main(args):
    if args.full or args.step == 'extract':
        orsan_conn = pyodbc.connect(Settings.DB_ORSAN)

        if args.docs:
            print('Extracting documents')
            extract_docs(orsan_conn)

        for item in ['clients', 'poliza', 'endoso']:
            print(f'Extracting {item}')
            extract(orsan_conn, item)

    users_conn = psycopg2.connect(Settings.DB_USER)
    poliza_conn = psycopg2.connect(Settings.DB_POLIZA)

    print('Transform clients')
    transform_clients()

    print('Load clients')
    load_clients(users_conn)

    print('Transform polizas')
    transform_polizas(poliza_conn)

    print('Load polizas')
    load_polizas(poliza_conn)

    print('Transform endosos')
    transform_endosos()

    print('Load endosos')
    load_endosos(poliza_conn)

    if args.docs:
        print('Transform docs')
        transform_docs()

        print('Please import documents from the poliza app')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Migrate data')
    parser.add_argument(
        '--full',
        nargs='?',
        const=True,
        default=False
    )
    parser.add_argument(
        '--step',
        choices=['extract', 'load'],
        default='extract'
    )
    parser.add_argument(
        '--docs',
        nargs='?',
        const=True,
        default=False
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
