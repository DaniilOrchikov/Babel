from flask import Flask, make_response
from requests import get
from flask import request
from flask import redirect
from data import db_session
from data.quick_saves import QuickSaves
from data.users import User
from flask_restful import Api, reqparse
from flask import render_template
from library_of_babel import babel
from forms.user import LoginForm
from forms.user import RegisterForm
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from api.api import BookList, RandomPage, Page

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = '/static/search_image'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
api.add_resource(BookList, '/api/book_list/<string:address>')
api.add_resource(Page, '/api/page/<string:r_type>/<string:request_str>')
api.add_resource(RandomPage, '/api/random_page')

scale = 2.2


def main():
    db_session.global_init("db/data_base.db")
    app.run(port=8080, host='127.0.0.1')


login_manager = LoginManager()
login_manager.init_app(app)


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        elif len(room) % 3 != 0:
            return render_template('browse.html', title='Библиотека',
                                   message_room="Некорректные данные номера "
                                                "комнаты(количество символов должно быть кратно 3)")
        elif not all(map(lambda x: x in babel.used_symbols, room)):
            return render_template('browse.html', title='Библиотека',
                                   message_room=f"Некорректные данные номера комнаты(можно использовать "
                                                f"только символы: {babel.used_symbols})")
        elif not (0 < int(page) < 411) or not (page.isdigit()):
            return render_template('browse.html', title='Библиотека',
                                   message_page="Некорректные данные номера страницы")
        id = get(f'http://127.0.0.1:8080/api/page/a/{room}-{wall}-{shelf}-{book}-{page}').json()['id']
        return redirect(f'/image{id}')


@app.route('/image<string:id>', methods=['POST', 'GET'])
def image(id):
    """выбранная/случайная книга"""
    if request.method == 'GET':
        left = request.args.get('left')
        right = request.args.get('right')
        full_left = request.args.get('full-left')
        full_right = request.args.get('full-right')
        save_id = int(request.cookies.get('id', 0))
        if not save_id:
            id = save_id
        db_sess = db_session.create_session()
        save = db_sess.query(QuickSaves).filter(QuickSaves.id == int(id)).first()
        data = {'image': save.image,
                'address': save.address,
                'title': save.title}
        page = data['address'].split("-")[-1]
        if left is not None and int(page) > 1:
            id = get(f'http://127.0.0.1:8080/api/page/a/{"-".join(data["address"].split("-")[:-1]) + "-" + str((int(page) - 1))}').json()['id']
            db_sess.delete(save)
            db_sess.commit()
            return redirect(f'/image{id}')
        elif right is not None and int(page) < babel.page:
            id = get(f'http://127.0.0.1:8080/api/page/a/{"-".join(data["address"].split("-")[:-1]) + "-" + str((int(page) + 1))}').json()['id']
            db_sess.delete(save)
            db_sess.commit()
            return redirect(f'/image{id}')
        elif full_left is not None:
            id = get(f'http://127.0.0.1:8080/api/page/a/{"-".join(data["address"].split("-")[:-1]) + "-1"}').json()['id']
            db_sess.delete(save)
            db_sess.commit()
            return redirect(f'/image{id}')
        elif full_right is not None:
            id = get(f'http://127.0.0.1:8080/api/page/a/{"-".join(data["address"].split("-")[:-1]) + "-410"}').json()['id']
            db_sess.delete(save)
            db_sess.commit()
            return redirect(f'/image{id}')
        res = make_response(render_template('book.html', title='Книга', picture_name=data['image'], number_page=page,
                                            name=data['title'], width=babel.width * scale, height=babel.height * scale))
        save_id = int(request.cookies.get('id', 0))
        if not save_id:
            res.set_cookie('id', str(save.id))
        return res


@app.route('/account')
def personal_account():
    """страница с личным кабинетом: все сохраненные фотографии"""
    return render_template('account.html', title='Личный аккаунт')


@app.route('/random_book')
def random_book():
    id = get(f'http://127.0.0.1:8080/api/random_page').json()['id']
    return redirect(f'/image{id}')


@app.route('/search', methods=['POST', 'GET'])
def search():
    """страница с поиском картинки"""
    if request.method == 'GET':
        return render_template('search.html', title='Поиск картинки')
    elif request.method == 'POST':
        radio = request.form.get('flexRadioDefault')
        file = request.files['file']
        id = get(f'http://127.0.0.1:8080/api/page/im/' + ('ex' if radio == 'radio1' else 'n'),
                 files={'file': file}).json()['id']
        return redirect(f'/image{id}')


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


if __name__ == '__main__':
    main()
