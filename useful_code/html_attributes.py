from flask import Flask

app = Flask(__name__)


@app.route('/')
def new_page():
    """# создает отдельную вкладку с сайтом библиотеки"""
    return """<a href="https://libraryofbabel.info/" target="_blank">Вавилонская библиотека</a>"""


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
