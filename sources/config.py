from decouple import config


class Settings:
    DRIVER = config('DRIVER')
    DATABASE = config('DATABASE')
    USER = config('DB_USER')
    PASSWORD = config('PASSWORD')

    USER_DB_HOST = config('USER_DB_HOST')
    USER_DB_PORT = config('USER_DB_PORT')
    USER_DB_DATABASE = config('USER_DB_DATABASE')
    USER_DB_USER = config('USER_DB_USER')
    USER_DB_PASSWORD = config('USER_DB_PASSWORD')

    POLIZA_DB_HOST = config('POLIZA_DB_HOST')
    POLIZA_DB_PORT = config('POLIZA_DB_PORT')
    POLIZA_DB_DATABASE = config('POLIZA_DB_DATABASE')
    POLIZA_DB_USER = config('POLIZA_DB_USER')
    POLIZA_DB_PASSWORD = config('POLIZA_DB_PASSWORD')
