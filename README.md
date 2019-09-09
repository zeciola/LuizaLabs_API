# LuizaLabs API

## Run Project:
```sh
export FLASK_APP=app/main.py
export FLASK_ENV=Development
export FLASK_DEBUG=True

flask run
```

## Use Postman collection:
```Luizalabs_Flask_API.postman_collection.json```

## Flask Routes:
```
Endpoint                                    Methods  Rule
------------------------------------------  -------  ----------------------------------------------
auth.login                                  POST     /api/login
client.client_change_by_email               PUT      /api/client/change/email/
client.client_delete_by_email               DELETE   /api/client/delete/email/
client.client_register                      POST     /api/client/register
client.client_show_by_email                 POST     /api/client/show/email
product.favorite_product_change             PUT      /api/product/favorite/change/
product.favorite_product_delete             DELETE   /api/product/favorite/delete/
product.favorite_product_register           POST     /api/product/favorite/register
product.favorite_product_show_by_client_id  GET      /api/product/favorite/show/client/<identifier>
product.product_change_by_title             PUT      /api/product/change/title/
product.product_delete_by_title             DELETE   /api/product/delete/title/
product.product_register                    POST     /api/product/register
product.product_show_by_id                  GET      /api/product/<identifier>
product.product_show_by_title               POST     /api/product/show/title
static                                      GET      /static/<path:filename>
```

## Create db and make migrations:
```sh
export FLASK_APP=app/main.py
export FLASK_ENV=Development
export FLASK_DEBUG=True

flask db init
flask db migrate
flask db upgrade
```

## How to run the tests:
```sh
export FLASK_APP=app/main.py
export FLASK_ENV=Development
export FLASK_DEBUG=True

pytest tests/*
```
