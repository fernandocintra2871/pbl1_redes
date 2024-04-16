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

def get_command(sensor):
    while True:
        entry = input("Digite um comando: ")
        command, value = entry.split()
        if command == "temp":
            sensor.set_temp(int(value))
            
            
sensor = Sensor()

thread_command = threading.Thread(target=get_command, args=(sensor,))
thread_command.daemon = True
thread_command.start()

HOST = '127.0.0.1' 
PORT = 12344        

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect((HOST, PORT))

# Iniciando a comunicação com o broker
data = {"state": sensor.get_state(), "temperature": sensor.get_temp()}
msg = json.dumps(data)
s.sendall(msg.encode())