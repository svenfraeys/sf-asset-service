# sf-asset-service

sfassetservice is a REST api that allows you to author, edit, query and delete digital assets

## Installation

Inside the directory run pip install

```
pip install .
```

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

