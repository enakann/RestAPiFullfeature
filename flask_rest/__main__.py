#!/usr/bin/env python3

from app import app


def main():
    # app = connexion.App(__name__, specification_dir='./swagger/')
    # app.app.json_encoder = encoder.JSONEncoder
    # app.add_api('swagger.yaml', arguments={'title': 'Swagger Petstore'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
