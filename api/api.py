from flask import jsonify
from flask_restful import Resource

from library_of_Babel import babel


class BookList(Resource):
    def get(self, address):
        titles = [babel.get_title(address + '-' + str(i)) for i in range(babel.volume)]
        return jsonify({'titles': titles})


class Page(Resource):
    def get(self, r_type, request_str):
        if r_type == 'im':
            image = request_str
            # магия
            search_str, width, height = babel.create_str(image)
            address = babel.search(search_str, width, height)
            title = babel.get_title(address)
            image = babel.create_im(address, title + address.split('-')[-1])
            # магия
            return jsonify(
                {
                    'image': image,
                    'address': address,
                    'title': title
                }
            )
        elif r_type == 'a':
            address = request_str
            title = babel.get_title(address)
            image = babel.create_im(address, title)
            # магия
            return jsonify(
                {
                    'image': image,
                    'address': address,
                    'title': title
                }
            )


class RandomPage(Resource):
    def get(self):
        address = babel.get_random()
        title = babel.get_title(address)
        image = babel.create_im(address, title)
        # магия
        return jsonify(
            {
                'image': image,
                'address': address,
                'title': title
            }
        )
