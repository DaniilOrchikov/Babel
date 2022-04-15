import base64
from flask import Flask, render_template, request
from flask_restful import Api
from werkzeug.utils import redirect

from api.api import BookList, Page, RandomPage
from data import db_session
from requests import get

from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
api.add_resource(BookList, '/api/book_list/<string:address>')
api.add_resource(Page, '/api/page/<string:r_type>/<string:request_str>')
api.add_resource(RandomPage, '/api/random_page')


# data = get('http://127.0.0.1:5000/api/random_page').json()['image']
# return f'<img src={data}>'  # отображение картинки


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/search_im', methods=['GET', 'POST'])
def search_im():
    """Страница с поиском по картинке"""
    if request.method == 'GET':
        return render_template('search_im.html')
    else:
        f = request.files['file'].read()
        image = base64.b64encode(f).decode()
        data = get('http://127.0.0.1:5000/api/page/im/' + image).json()
        return redirect('/book/' + data['address'])


@app.route('/browse')
def browse():
    """Страница с самой библиотекой(можно выбрать комнату шкаф и тд)"""
    return render_template('browse.html')


@app.route('/image/<string:address>')
def image(address):
    """Страница со страницей, которая расположена по адресу
На эту же страницу будет переход при нажатии на random"""


@app.route('/personal_account')
def personal_account():
    """Личный кабинет"""
    im_list = current_user.im_list.split('┫ ┫')
    data_list = []
    for i in im_list:
        data_list.append(get('http://127.0.0.1:5000/api/page/a/' + i).json())
    return render_template('personal_account.html', name=current_user.name,
                           email=current_user.email) + ' '.join(
        [render_template('personal_account_saved_image.html', image=i['image'],
                         name=i['title']) for i in data_list])


@app.route('/info')
def info():
    """Страница с информацией о сайте"""
    return render_template('info.html')


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