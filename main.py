from flask import Flask
from flask_restful import Api
from requests import get

from api.api import GetTitle

app = Flask(__name__)
api = Api(app)


def main():
    app.run()


@app.route('/')
def index():
    return 'Начальная страница'


@app.route('/search')
def search():
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
