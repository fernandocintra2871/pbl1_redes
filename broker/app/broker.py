from flask import Flask, jsonify, request
import socket
import threading
import json
import time

color_green = "\033[92m"
color_red =  "\033[91m"
color_white = "\033[0m"

app = Flask(__name__)

data = {} # Guarda a temperatura e o estado de cada dispositivo/sensor em um dicionario
devices = {} # Guarda o IP e PORTA de cada dispositivo
conns = {} # Guarda as conexões TCP feitas com cada dispositivo
commands = [] # Guarda os comandos enviados pela aplicação até serem enviados para cada dispositivo

# API
@app.route('/commands', methods=['POST']) # Adiciona um comando a lista de comandos a serem enviados para os dispoitivos
def post_command():
    if request.method == 'POST':
        new_command = request.json
        commands.append(new_command)
        print(commands)
        return jsonify(commands), 201

@app.route('/sensors', methods=['GET']) # Retorna os dados de todos sensores conectados ao Broker
def get_sensors():
    if request.method == 'GET':
        return jsonify(data)

# Função para obter a chave pelo valor
def find_key(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

# Função que recebe os dados via UDP continuamente
def udp_receiver(s):
    id = 0

    while True:
        msg, addr = s.recvfrom(1024)
        msg = msg.decode()
        msg = json.loads(msg)
        if addr not in devices.values(): # Caso o dado recebido venham de um dispositivo não cadastrado
            devices[id] = addr # É feito o cadastro do dispositivo
            data[id] = msg
            print(f"{color_green}Novo dispositivo cadastrado {addr} como Sensor {id}")
            print(f"{msg} recebidos de Sensor {id} {addr} via UDP {color_white}")
            id += 1
        else:
            #index = devices.index(addr)
            index = find_key(devices, addr)
            data[index] = msg
            print(f"{color_green}{msg} recebidos do Sensor {index} {addr} via UDP{color_white}")

# Função que observa o socket continuamente para aceitar novas conexões TCP
def tcp_listener(s):
    id = 0
    while True:
        s.listen()
        conn, addr = s.accept()
        msg = conn.recv(1024)
        if msg.decode() == 'init': # Caso a mensagem da primeira conexão TCP seja 'init'
            conns[id] = conn # A nova conexão TCP é adicionada a lista de conexões
            id += 1

# Função que envia os comandos feitos pela Aplicação para os dispostiivos
def tcp_sender(s):
    while True: # Enquanto tiver comandos pendentes na lista commands esses comandos são enviados para o respectivo dispositivo
        if len(commands) > 0:
            conns[commands[0]['sensor']].send(commands[0]['command'].encode())
            print(f"{color_green}Comando {commands[0]['command']} enviado via TCP para o Sensor {commands[0]['sensor']} {devices[commands[0]['sensor']]}{color_white}")
            commands.pop(0)

# Função que checa se os dispositivos ainda estão conectados ao broker
def check_device_conn():
    while True:
        time.sleep(3)
        for i in conns.copy().keys():
            try:
                conns[i].send("test".encode())
                conns[i].settimeout(2)
                msg = conns[i].recv(1024)
                if not msg:
                    print(f"{color_red}A conexão com o Sensor {i} foi perdida{color_white}")
                    data.pop(i)
                    devices.pop(i)
                    conns.pop(i)
                if i not in data.keys():
                    print(f"{color_green}A conexão com o Sensor {i} foi recuperada{color_white}")
                    conns[i].send("reconnect".encode())
            except:
                if i in data.keys():
                    print(f"{color_red}A conexão com o Sensor {i} foi perdida{color_white}")
                    data.pop(i)

# Função que retorna o IP da maquina
def get_ip():
    hostname = socket.gethostname()    
    ip = socket.gethostbyname(hostname)
    return ip

host = get_ip()
print(f"Broker operando no ip: {color_green}{get_ip()}{color_white}")

# Recebimento de dados dos dispositivos via UDP
HOST_UDP = host
PORT_UDP = 12344  

udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket UDP
udp_s.bind((HOST_UDP, PORT_UDP)) # Associa o socket ao IP e PORTA passados como parametro
#print(f"Servidor UDP esperando na porta {PORT_UDP}...")

thread_udp_receiver = threading.Thread(target=udp_receiver, args=(udp_s,)) # Cria a thread para receber dados dos dispositivos via UDP
thread_udp_receiver.start() # Inicia a thread

# Envio de dados para os dispositivos via TCP
HOST_TCP = host
PORT_TCP = 12343

tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP
tcp_s.bind((HOST_TCP, PORT_TCP)) # Associa o socket ao IP e PORT passados como parametro
#print(f"Servidor TCP esperando na porta {PORT_TCP}...")

thread_tcp_listener = threading.Thread(target=tcp_listener, args=(tcp_s,)) # Cria a thread para aceitar novas conexões TCP
thread_tcp_listener.start()

thread_tcp_sender = threading.Thread(target=tcp_sender, args=(tcp_s,)) # Cria a thread para enviar dados via TCP para os dispositivos
thread_tcp_sender.start()

t_check_device_conn = threading.Thread(target=check_device_conn) # Cria a thread que checa se os dispositivos ainda estão conectados
t_check_device_conn.start()

# Inicia a API
app.run(host=host, port=12345)