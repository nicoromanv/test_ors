### Setup
Setup the SQL Server client according to your environment: https://github.com/mkleehammer/pyodbc/wiki

Install requirements
```.bash
pip install -r requirements.txt
```

Create an `.env` file inside `sources` with the db configurations
```.env
DRIVER=
DATABASE=
DB_USER=
PASSWORD=

USER_DB_HOST=
USER_DB_PORT=
USER_DB_DATABASE=
USER_DB_USER=
USER_DB_PASSWORD=

POLIZA_DB_HOST=
POLIZA_DB_PORT=
POLIZA_DB_DATABASE=
POLIZA_DB_USER=
POLIZA_DB_PASSWORD=
```

### Migrate the data

The `main.py` script takes two optional arguments. By default, it runs only the data transformation and load.
With the `--full` flag, it also extracts the data from the original database, except the endoso documents.
To extract these, add the `--docs` flag

```.bash
python main.py  # Transform and loads the previously extracted data
python main.py --full  # Runs the full ETL process, except document extraction
python main.py --full --docs  # Runs the full ETL process, including documents
```
