import os
import socket
import threading
import json

host = os.environ.get("ip_broker") # Pega o IP do broker passado como váriavel de ambiente Docker

HOST_TCP = host
PORT_TCP = 12343

HOST_UDP = host
PORT_UDP = 12344  

# Classe feita para organizar os dados do Dispositivo no formato de um objeto
class Sensor:
    def __init__(self):
        self.temp = 0
        self.state = False
    
    def get_temp(self):
        return self.temp

    def set_temp(self, temp):
        self.temp = temp

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

# Função feita para verificar se um número é um float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
            
# Função que envia através de um socket UDP
def send_data(s, sensor):
    data = {"state": sensor.get_state(), "temp": sensor.get_temp()}
    msg = json.dumps(data) # Converte os dados para json
    s.sendall(msg.encode()) # Envia os dados para os disposistivos conectados ao socket

# Função que recebe dados através de um socket TCP
def receiver_data(sensor, s_udp, s_tcp):
    while True:
        msg = ""
        try:
            msg = s_tcp.recv(1024).decode() # Lê os dados recebidos
            if not msg:
                s_tcp.close()
                s_tcp = tcp_init()
                send_data(s_udp, sensor)
                print("\nPressione ENTER para digitar um comando.")
        except: # Caso perca a conexão com o Broker tenta criar uma nova
            s_tcp.close()
            s_tcp = tcp_init()
            send_data(s_udp, sensor)
            print("\nPressione ENTER para digitar um comando.")
        if msg == 'ligar':
            sensor.set_state(True)
            send_data(s_udp, sensor) # Envia os dados atualizados
            print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")

        elif msg == 'desligar':
            sensor.set_state(False)
            send_data(s_udp, sensor) # Envia os dados atualizados
            print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")

        elif msg == 'test':
            s_tcp.sendall(b'test')

        elif msg == 'reconnect':
            send_data(s_udp, sensor) # Envia os dados atualizados

# Função que inicia a conexão TCP para o recebimento de dados
def tcp_init():
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("\nTentando conexão com o Broker...")
    broker_found = False
    while broker_found == False: # Fica em loop até  se conectar com o Broker
        try:
            s_tcp.connect((HOST_TCP, PORT_TCP))
        except:
            pass
        else:
            broker_found = True

    s_tcp.sendall(b'init')

    print("\nDispositivo conectado ao Broker!")
    return s_tcp


# Função que inicia a conexão UDP para o envio de dados     
def udp_init():
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket UDP

    s_udp.connect((HOST_UDP, PORT_UDP)) # Conecta o socket a HOST e a PORT indicada

    # Primeira comunicação UDP para cadastro do dispositivo no Broker
    data = {"state": sensor.get_state(), "temp": sensor.get_temp()}
    msg = json.dumps(data) # Converte para json
    s_udp.sendall(msg.encode()) # Envia os dados atrves do socket

    return s_udp

# Instancia o objeto Sensor
sensor = Sensor()

# Conexão TCP para o recebimento de dados
s_tcp = tcp_init()

# Conexão UDP para o envio de dados      
s_udp = udp_init()

# Criação de uma thread para ficar recebendo comandos do broker
thread_receiver = threading.Thread(target=receiver_data, args=(sensor, s_udp, s_tcp,)) 
thread_receiver.start()

# Interface para entrada de comandos para o Dispositivo
print('\nSensor')
print("\nComandos:\n. ligar\n. desligar\n. temp [valor]")
while True:
    input("\nPressione ENTER para digitar um comando.")
    entry = input("\nDigite um comando: ")
    entry = entry.split()
    if len(entry) == 2 and entry[0] == "temp" and isfloat(entry[1]):
        sensor.set_temp(float(entry[1]))
        if sensor.get_state() == True:
            send_data(s_udp, sensor)
        print(f"\nTemperatura atualizada para {sensor.get_temp()}")
    elif len(entry) == 1 and entry[0] == "ligar" and sensor.get_state() != True:
        sensor.set_state(True)
        send_data(s_udp, sensor)
        print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")
    elif len(entry) == 1 and entry[0] == "desligar" and sensor.get_state() != False:
        sensor.set_state(False)
        send_data(s_udp, sensor)
        print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")
    elif len(entry) == 1 and entry[0] == "ligar" and sensor.get_state() == True:
        print("\nO sensor já está ligado!")
    elif len(entry) == 1 and entry[0] == "desligar" and sensor.get_state() == False:
        print("\nO sensor já está desligado!")
    else:
        print(f"\nComando inválido!")