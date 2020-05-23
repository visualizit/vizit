import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_socketio import SocketIO

NAMESPACE = '/raft-monitor'

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)


@app.route('/monitor/action', methods=['POST'])
def monitor_action():
    action = request.get_json()
    return jsonify(action)


@app.route('/', methods=['GET'])
def index():
    socket_io.emit('update monitor', f'now: {datetime.now()}', namespace=NAMESPACE)
    return 'hello'


@socket_io.on('client action', namespace=NAMESPACE)
def handle_client_action(json):
    print(f'client action: {str(json)}')


if __name__ == '__main__':
    socket_io.run(app)
