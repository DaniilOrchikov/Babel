from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from data import db_session
from data.users import User
from flask_restful import Api
from flask import render_template
from forms.user import RegisterForm
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from forms.user import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# api = Api(__name__)

def main():
    db_session.global_init("db/data_base.db")
    app.run(port=8080, host='127.0.0.1')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def home_page():
    """начальная страница"""
    return render_template('index.html', title='Главная страница страница')


@app.route('/information')
def info():
    """страница с информацией о сайте"""
    return render_template('info.html', title='Информация')


@app.route('/browse', methods=['POST', 'GET'])
def browse():
    """основная страница с библиотекой -> переход в def image()"""
    if request.method == 'GET':
        return render_template('browse.html', title='Библиотека')
    elif request.method == 'POST':
        """получаем номера стеллажей, полок и тд, после отправки формы пользователем"""
        room = request.form.get('room')
        wall = request.form.get('wall')
        shelf = request.form.get('shelf')
        book = request.form.get('book')
        page = request.form.get('page')
        if room == "":
            return render_template('browse.html', title='Библиотека',
                                   message="Введите номер комнаты")
        elif page == "":
            return render_template('browse.html', title='Библиотека',
                                   message="Введите номер страницы")
        elif not (room.isdigit()):
            return render_template('browse.html', title='Библиотека',
                                   message_room="Некорректные данные номера полки(не натуральное число)")
        elif not (0 < int(page) < 410) or not (room.isdigit()):
            return render_template('browse.html', title='Библиотека',
                                   message_page="Некорректные данные номера страницы")
    # здесь алгоритм, который генерирует картинку
    # получаем переменную с путем к файлу name
    # пока заглушка стоит на картинку из директории
    return render_template('book.html', title='Поиск картинок', picture_name="static/img/telegram.png")


@app.route('/search')
def search():
    """страница с поиском картинки"""
    return render_template('search.html', title='Поиск картинок')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():  # регистрация
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
        return redirect('/sign_in')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/image')
def image():
    """выбранная книга"""
    return render_template('book.html', title='Выбранная картинка')


@app.route('/account')
def personal_account():
    """страница с личным кабинетом: все сохраненные фотографии"""
    return render_template('account.html', title='Личный аккаунт')


@app.route('/random_book')
def random_book():
    """"""
    return render_template('book.html', title='Личный аккаунт')


if __name__ == '__main__':
    main()
