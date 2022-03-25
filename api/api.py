from flask import jsonify
from flask_restful import Resource

from new_algoritm import babel


class GetTitle(Resource):
    def get(self, address):
        return jsonify({'title': babel.search_title(address)})
