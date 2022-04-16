from flask import jsonify
from flask_restful import Resource

from library_of_babel import babel


class BookList(Resource):
    def get(self, address):
        titles = [babel.get_title(address + '-' + str(i)) for i in range(babel.volume)]
        return jsonify({'titles': titles})


class Page(Resource):
    def get(self, r_type, request_str):
        if r_type == 'im':
            image = bytearray(request_str)
            search_str, width, height = babel.create_str(image)
            address = babel.search(search_str, width, height)
            title = babel.get_title(address)
            image = babel.create_im(address)
            image = image.decode()
            return jsonify(
                {
                    'image': f'data:image/jpeg;base64,{image}',
                    'address': address,
                    'title': title
                }
            )
        elif r_type == 'a':
            address = request_str
            title = babel.get_title(address)
            image = babel.create_im(address)
            image = image.decode()
            return jsonify(
                {
                    'image': f'data:image/jpeg;base64,{image}',
                    'address': address,
                    'title': title
                }
            )


class RandomPage(Resource):
    def get(self):
        address = babel.get_random()
        title = babel.get_title(address)
        image = babel.create_im(address)
        image = image.decode()
        return jsonify(
            {
                'image': f'data:image/jpeg;base64,{image}',
                'address': address,
                'title': title
            }
        )
