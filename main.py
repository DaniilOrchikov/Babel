from flask import Flask, render_template
from flask_restful import Api
from werkzeug.utils import redirect

from api.api import BookList, Page, RandomPage
from data import db_session
from requests import get

from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
api.add_resource(BookList, '/api/book_list/<string:address>')
api.add_resource(Page, '/api/page/<string:r_type>/<string:request_str>')
api.add_resource(RandomPage, '/api/random_page')


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/')
def index():
    # data = get('http://127.0.0.1:5000/api/random_page').json()['image']
    # return f'<img src={data}>'    отображение картинки
    return '1234567890'


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


@app.route('/personal_account')
def personal_account():
    return 'Личный кабинет'


@app.route('/info')
def info():
    return 'Страница с информацией о сайте'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
