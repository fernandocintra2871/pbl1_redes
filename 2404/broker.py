from flask import Flask, jsonify, request
import socket
import threading
import json


app = Flask(__name__)

data = []
devices = [] # hosts conectadas ao broker
conns = []
commands = []

@app.route('/commands', methods=['POST'])
def post_command():
    if request.method == 'POST':
        new_command = request.json
        commands.append(new_command)
        print(commands)
        return jsonify(commands), 201

@app.route('/sensors', methods=['GET'])
def get_sensors():
    if request.method == 'GET':
        return jsonify(data)

def udp():
    HOST = '127.0.0.1'
    PORT = 12344  

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print(f"Servidor UDP esperando na porta {PORT}...")

    while True:
        msg, addr = s.recvfrom(1024)
        msg = msg.decode()
        msg = json.loads(msg)
        if addr not in devices:
            devices.append(addr)
            data.append(msg)
            print(f"Nova conexão feita  com {addr}\nDados recebidos: {msg}")
        else:
            index = devices.index(addr)
            data[index] = msg
            print(f"{msg} recebidos de {addr}")

def tcp_listener(s):
    while True:
        s.listen()
        print("Aguardando conexão...")
        conn, addr = s.accept()
        msg = conn.recv(1024)
        if msg.decode() == 'init':
            conns.append(conn)
            print(f"Conexão TCP {conn} feita com {addr}")

def tcp_send(s):
    while True:
        if len(commands) > 0:
            conns[commands[0]['sensor']].send(commands[0]['command'].encode())
            print(f"Comando {commands[0]['command']} enviado para o Sensor {commands[0]['sensor']}")
            if commands[0]['command'] == 'desligar':
                data[commands[0]['sensor']]['state'] = False
            commands.pop(0)


thread_udp = threading.Thread(target=udp)
thread_udp.start()

HOST = '127.0.0.1'
PORT = 12343

tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_s.bind((HOST, PORT))

thread_tcp_listener = threading.Thread(target=tcp_listener, args=(tcp_s,))
thread_tcp_listener.start()

thread_tcp_send = threading.Thread(target=tcp_send, args=(tcp_s,))
thread_tcp_send.start()

app.run(host='127.0.0.1', port=12345)