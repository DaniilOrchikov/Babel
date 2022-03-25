from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(__name__)


def main():
    app.run()


@app.route('/')
def home_page():
    """начальная страница"""


@app.route('/information')
def info():
    """страница с информацией о сайте"""


@app.route('/library')
def library():
    """основная страница с библиотекой -> переход в def image()"""


@app.route('/search')
def search():
    """страница с поиском картинки"""


@app.route('/sing_up')
def sing_up():
    """страница с регистрацией"""


@app.route('/sing_in')
def sing_in():
    """страница с авторизацией"""


@app.route('/image')
def image():
    """случайно сгенерированная картинка/выбранная книга"""


@app.route('/account')
def personal_account():
    """страница с личным кабинетом: все сохраненные фотографии"""


if __name__ == '__main__':
    main()
