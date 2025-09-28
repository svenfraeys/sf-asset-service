# sf-asset-service

sfassetservice is a REST API that allows you to author, edit, query and delete digital assets.
This repository is experimental and and can be used as reference.

## Setup

Inside the directory run pip install

```
pip install .
```

create a .env file to connect a PostgreSQL database

Example:

```
DB_USERNAME=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_NAME=sfpd
DB_PORT=5432
SECRET_TOKEN=fake-super-secret-token
```

## installation

After that you will have to install the database models

Run this script to install the database tables and do any additional installation needed

```
sfassetservice initdb
sfassetservice install
```

## Running the application for development

run the server like this for development and live reload

```
uvicorn sfasset_service.main:app --reload
```

## Running the application for production

run the server for production

```
uvicorn sfasset_service.main:app 
```

