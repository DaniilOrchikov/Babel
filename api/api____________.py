from flask import jsonify
from flask_restful import Resource
from requests import get

from library_of_Babel import babel


class GetTitle(Resource):
    def get(self, address):
        return jsonify({'title': babel.get_title(address)})


class SearchTitle(Resource):
    def get(self, title):
        return jsonify({'address': babel.search_title(title)})


class Search(Resource):
    def get(self, search_str, width, height):
        random_address = babel.search(search_str, width, height)
        exactly_address = babel.search_exactly(search_str, width, height)
        return jsonify(
            {
                'random': {
                    'address': random_address,
                    'title': get('http://localhost:5000/api/get_title/' + random_address).json()['title']
                },
                'exactly': {
                    'address': exactly_address,
                    'title': get('http://localhost:5000/api/get_title/' + exactly_address).json()['title']
                }
            }
        )


class GetIm(Resource):
    def get(self, address, name):
        return jsonify({'image': babel.create_im(address, name)})


class GetRandomIm(Resource):
    def get(self, name):
        return jsonify({'image': babel.get_random_im(name)})
