from flask import Flask, jsonify, request
import socket
import threading
import json


app = Flask(__name__)

data = [
    {"state": True, "temperature": 22},
    {"state": False, "temperature": 21},
    {"state": True, "temperature": 27},
    {"state": False, "temperature": 19}
]

@app.route('/sensors', methods=['GET'])
def get_sensors():
    if request.method == 'GET':
        return jsonify(data)

@app.route('/sensors/<id>', methods=['PATCH'])
def patch_sensor(id):
    if request.method == 'PATCH':
        if int(id) >= 0 and int(id) < len(data):
            partial_data = request.json
            data[int(id)]['state'] = partial_data['state']
            return jsonify(data[int(id)])
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404

def udp():
    HOST = '127.0.0.1'
    PORT = 12344  

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print(f"Servidor UDP esperando na porta {PORT}...")

    while True:
        msg, addr = s.recvfrom(1024)
        data = msg.decode()
        data = json.loads(data)

        #print(f"Mensagem recebida de {addr}: {data}")

    

thread_udp = threading.Thread(target=udp)
thread_udp.daemon = True
thread_udp.start()

app.run(host='127.0.0.1', port=12345)