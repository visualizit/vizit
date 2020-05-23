import logging
import queue
from datetime import datetime
from flask import Flask, request, jsonify
from flask_socketio import SocketIO

NAMESPACE = '/raft-monitor'

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)
q = queue.Queue()


@app.route('/monitor/action', methods=['POST'])
def monitor_action():
    action = request.get_json()
    return jsonify(action)


@app.route('/view/status', methods=['POST'])
def view_status():
    leader = request.get_json()
    logging.info(f' got heartbeat from leader: {leader}')
    return {}


@app.route('/', methods=['GET'])
def index():
    q.put(f'ct: {datetime.now()}')
    socket_io.emit('update monitor', q.get(), namespace=NAMESPACE, callback=ack)
    return 'hello'


def ack():
    print('message was received!')


@socket_io.on('client action', namespace=NAMESPACE)
def handle_client_action(json):
    print(f'client action: {str(json)}')


if __name__ == '__main__':
    socket_io.run(app, port=8000)
