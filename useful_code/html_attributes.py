from flask import Flask

app = Flask(__name__)


@app.route('/')
def new_page():
    """# создает отдельную вкладку с сайтом библиотеки"""
    return """<a href="https://libraryofbabel.info/" target="_blank">Вавилонская библиотека</a>"""

@app.route('/greeting/<username>')
def greeting(username):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                   <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Привет, {username}</title>
                  </head>
                  <body>
                    <h1>Привет, {username}!</h1>
                  </body>
                </html>'''
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')


# <!DOCTYPE html>
# <html>
#   <head>
#     <meta charset="utf-8">
#     <title>Страница</title>
#   </head>
#   <body>
#     <h1>...</h1>
#     <p>...</p>
#   </body>
# </html>


# <!DOCTYPE html>
# <html lang="ru">
#   <head>
#     <meta charset="utf-8">
#     <meta name="keywords" content="вёрстка, HTML, CSS, блог">
#     <meta name="description" content="само описание">
#     <title>Сайт</title>
#     <link rel="stylesheet" href="outlines.css">
#   </head>
#   <body>
#     <header>
#       <h1>Сайт</h1>
#     </header>
#     <main>
#       <nav>
#         Навигация
#       </nav>
#       <section>
#         <p></p>
#       </section>
#       <section>
#         ...
#       </section>
#     </main>
#     <footer>
#       Подвал сайта
#     </footer>
#   </body>
# </html>
