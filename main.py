from flask import Flask
from flask_restful import Api
from requests import get

from api.api import GetTitle, SearchTitle, Search, GetIm, GetRandomIm

app = Flask(__name__)
api = Api(app)
api.add_resource(GetTitle, '/api/get_title/<string:address>')
api.add_resource(SearchTitle, '/api/search_title/<string:title>')
api.add_resource(Search, '/api/search/<string:search_str>/<int:width>/<int:height>')
api.add_resource(GetIm, '/api/create_im/<string:address>/<string:name>')
api.add_resource(GetRandomIm, '/api/get_random_im/<string:name>')


def main():
    app.run()


@app.route('/')
def index():
    return 'Начальная страница'


@app.route('/search_im')
def search_im():
    return 'Страница с поиском по картинке'


@app.route('/browse')
def browse():
    return 'Страница с самой библиотекой(можно выбрать комнату шкаф и тд)'


@app.route('/book/<string:address>')
def book(address):
    return f'''Страница со страницей, которая расположена по адресу{address}
На эту же страницу будет переход при нажатии на random'''


@app.route('/sign_up')
def sign_up():
    return 'Страница для создания нового пользователя'


@app.route('/sign_in')
def sign_in():
    return 'Страница для входа в учетную запись'


@app.route('/personal_account')
def personal_account():
    return 'Личный кабинет'


@app.route('/info')
def info():
    return 'Страница с информацией о сайте'


if __name__ == '__main__':
    main()
