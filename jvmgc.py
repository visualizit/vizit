import logging
import threading

from flask import Flask
from flask_socketio import SocketIO
from kafka import KafkaConsumer

NAMESPACE = '/jvm-monitor'

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)


@app.route('/monitor/heartbeat', methods=['GET'])
def monitor_heartbeat():
    logging.info(f'heartbeat')
    socket_io.emit('update jvm', "heartbeat", namespace=NAMESPACE)
    return "OK"


class Emit(threading.Thread):
    def run(self) -> None:
        socket_io.emit('update heap', "update heap begin", namespace=NAMESPACE)


class HeapMonitor(threading.Thread):

    def run(self):
        logging.info(f'start to monitor heap')
        consumer = KafkaConsumer('jvm', group_id='vizit')
        # socket_io.emit('update heap', "update heap begin", namespace=NAMESPACE)
        for msg in consumer:
            logging.info(f'kafka: {msg}')
            # socket_io.emit('update heap', str(msg.value), namespace=NAMESPACE)
            Emit().start()


@socket_io.on('client action', namespace=NAMESPACE)
def handle_client_action(data):
    logging.info(f'client action: {str(data)}')
    HeapMonitor().start()


if __name__ == '__main__':
    socket_io.run(app)
