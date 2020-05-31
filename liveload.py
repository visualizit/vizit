from flask import Flask
from livereload import Server

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()
