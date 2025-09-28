# sf-asset-service

this is the server side of SFAsset to auther, edit, query and delete assets

## Installation

inside the directory run pip install

```
pip install .
```

After that you will have to install the database models

Run this script to drop and install the table

```
python dbreset.py
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

