FROM python:3.7.3-stretch

WORKDIR /src/

COPY requirements.txt .

RUN apt-get update && apt-get install apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && pip install --no-cache-dir -r requirements.txt

CMD bash
