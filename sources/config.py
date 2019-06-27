from decouple import config


class Settings:

    DB_ORSAN = f'DSN={config("DRIVER")};' \
        f'DATABASE={config("DATABASE")};' \
        f'UID={config("USER")};' \
        f'PWD={config("PASSWORD")}'

    DB_USER = f'host={config("USER_DB_HOST")} ' \
        f'port={config("USER_DB_PORT")} ' \
        f'dbname={config("USER_DB_DATABASE")} ' \
        f'user={config("USER_DB_USER")} ' \
        f'password={config("USER_DB_PASSWORD")}'

    DB_POLIZA = f'host={config("POLIZA_DB_HOST")} ' \
        f'port={config("POLIZA_DB_PORT")} ' \
        f'dbname={config("POLIZA_DB_DATABASE")} ' \
        f'user={config("POLIZA_DB_USER")} ' \
        f'password={config("POLIZA_DB_PASSWORD")}'
