from flask import Flask
from livereload import Server
from kafka import KafkaConsumer

app = Flask(__name__)


@app.route('/')
def hello_world():
    consumer = KafkaConsumer('jvm', group_id='vizit')
    for msg in consumer:
        print(msg)
    return 'Hello, World!'


if __name__ == '__main__':
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()
