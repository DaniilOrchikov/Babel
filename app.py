from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from flask_restful import Api
from flask import render_template
from forms.user import SingInForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# api = Api(__name__)

def main():
    # db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def home_page():
    """начальная страница"""
    return render_template('index.html', title='Главная страница страница')


@app.route('/information')
def info():
    """страница с информацией о сайте"""
    return render_template('info.html', title='Главная страница страница')


@app.route('/library')
def library():
    """основная страница с библиотекой -> переход в def image()"""
    return render_template('library.html', title='Библиотека')


@app.route('/search')
def search():
    """страница с поиском картинки"""
    return render_template('search.html', title='Поиск картинок')


@app.route('/sing_up', methods=['GET', 'POST'])
def sing_up():
    """страница с регистрацией"""
    return render_template('sing_up.html', title='Поиск картинок')


@app.route('/sing_in', methods=['GET', 'POST'])
def sing_in():
    """страница с авторизацией"""
    form = SingInForm()
    if form.validate_on_submit():
        return redirect('/account')
    return render_template('sing_in.html', title='Авторизация', form=form)


@app.route('/image/<string:address>')
def image():
    """случайно сгенерированная картинка/выбранная книга"""
    return render_template('adress.html', title='Поиск картинок')


@app.route('/account')
def personal_account():
    """страница с личным кабинетом: все сохраненные фотографии"""
    return render_template('account.html', title='Личный аккаунт')


if __name__ == '__main__':
    main()