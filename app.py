from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from data import db_session
from data.users import User
from flask_restful import Api
from flask import render_template
from forms.user import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# api = Api(__name__)

def main():
    db_session.global_init("db/data_base.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def home_page():
    """начальная страница"""
    return render_template('index.html', title='Главная страница страница')


@app.route('/information')
def info():
    """страница с информацией о сайте"""
    return render_template('info.html', title='Информация')


@app.route('/browse')
def browse():
    """основная страница с библиотекой -> переход в def image()"""
    return render_template('browse.html', title='Библиотека')


@app.route('/search')
def search():
    """страница с поиском картинки"""
    return render_template('search.html', title='Поиск картинок')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sing_in():
    """страница с авторизацией"""
    # if form.validate_on_submit():
    #     return redirect('/account')
    # return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/image/<string:address>')
def image():
    """странца с выбранной книгой"""
    return render_template('adress.html', title='Поиск картинок')


@app.route('/account')
def personal_account():
    """страница с личным кабинетом: все сохраненные фотографии"""
    return render_template('account.html', title='Личный аккаунт')


if __name__ == '__main__':
    main()
