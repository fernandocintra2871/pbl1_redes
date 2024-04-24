from time import sleep
import socket
import threading
import json


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

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_command(sensor):
    while True:
        print(f"\nEstado: {'Ligado' if sensor.get_state() else 'Desligado'}\nTemperatura: {sensor.get_temp()}")
        print("\nComandos:\n. ligar\n. desligar\n. temp [valor]")
        entry = input("\n Digite um comando: ")
        entry = entry.split()
        if len(entry) == 2 and entry[0] == "temp" and isfloat(entry[1]):
            sensor.set_temp(float(entry[1]))
            print(f"\nTemperatura atualizada para {sensor.get_temp()}")
        elif len(entry) == 1 and entry[0] == "ligar" and sensor.get_state() != True:
            sensor.set_state(True)
            print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")
        elif len(entry) == 1 and entry[0] == "desligar" and sensor.get_state() != False:
            sensor.set_state(False)
            print(f"\nEstado atualizada para {'Ligado' if sensor.get_state() else 'Desligado'}")
        elif len(entry) == 1 and entry[0] == "ligar" and sensor.get_state() == True:
            print("\nO sensor já está ligado!")
        elif len(entry) == 1 and entry[0] == "desligar" and sensor.get_state() == False:
            print("\nO sensor já está desligado!")
        else:
            print("\nComando inválido!")
            
def send_data(sensor):  
    HOST = '127.0.0.1' 
    PORT = 12344        

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((HOST, PORT))

    # Primeira comunicação
    data = {"state": sensor.get_state(), "temp": sensor.get_temp()}
    msg = json.dumps(data)
    s.sendall(msg.encode())

    while True:
        if sensor.get_state():
            data = {"state": sensor.get_state(), "temp": sensor.get_temp()}
            msg = json.dumps(data)
            s.sendall(msg.encode())
            sleep(3)

def receiver_data(sensor):
    HOST = '127.0.0.1'
    PORT = 12343

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall(b'init')

    while True:
        msg = s.recv(1024).decode()
        if msg == 'ligar':
            sensor.set_state(True)
        elif msg == 'desligar':
            sensor.set_state(False)

sensor = Sensor()

thread_command = threading.Thread(target=get_command, args=(sensor,))
thread_command.start()

thread_send = threading.Thread(target=send_data, args=(sensor,))
thread_send.start()

thread_receiver = threading.Thread(target=receiver_data, args=(sensor,))
thread_receiver.start()