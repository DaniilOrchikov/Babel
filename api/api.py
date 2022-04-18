import base64

import werkzeug.datastructures
from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.quick_saves import QuickSaves
from library_of_babel import babel

parser = reqparse.RequestParser()
parser.add_argument('file', type=werkzeug.datastructures.FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')


class BookList(Resource):
    def get(self, address):
        titles = [babel.get_title(address + '-' + str(i)) for i in range(babel.volume)]
        return jsonify({'titles': titles})


class Page(Resource):
    # def post(self, r_type, request_str):
    #     args = parser.parse_args()
    #     file = args['file'].read()
    #
    #     image = bytearray(file)
    #     search_str, width, height = babel.create_str(image)
    #     address = babel.search(search_str, width, height)
    #     title = babel.get_title(address)
    #     image = babel.create_im(address)
    #     image = image.decode()
    #     return jsonify(
    #         {
    #             'image': f'data:image/jpeg;base64,{image}',
    #             'address': address,
    #             'title': title
    #         }
    #     )

    def get(self, r_type, request_str):
        if r_type == 'im':
            args = parser.parse_args()
            file = args['file'].read()
            image = bytearray(file)
            search_str, width, height = babel.create_str(image)
            if request_str == 'ex':
                address = babel.search_exactly(search_str, width, height)
            else:
                address = babel.search(search_str, width, height)
            title = babel.get_title(address)
            image = babel.create_im(address)
            image = image.decode()

            db_sess = db_session.create_session()
            quick_save = QuickSaves(image=f'data:image/jpeg;base64,{image}',
                                    address=address,
                                    title=title)
            db_sess.add(quick_save)
            db_sess.commit()
            return jsonify(
                {
                    'id': quick_save.id
                }
            )
        elif r_type == 'a':
            address = request_str
            title = babel.get_title(address)
            image = babel.create_im(address)
            image = image.decode()

            db_sess = db_session.create_session()
            quick_save = QuickSaves(image=f'data:image/jpeg;base64,{image}',
                                    address=address,
                                    title=title)
            db_sess.add(quick_save)
            db_sess.commit()
            return jsonify(
                {
                    'id': quick_save.id
                }
            )


class RandomPage(Resource):
    def get(self):
        address = babel.get_random()
        title = babel.get_title(address)
        image = babel.create_im(address)
        image = image.decode()

        db_sess = db_session.create_session()
        quick_save = QuickSaves(image=f'data:image/jpeg;base64,{image}',
                                address=address,
                                title=title)
        db_sess.add(quick_save)
        db_sess.commit()
        return jsonify(
            {
                'id': quick_save.id
            }
        )
