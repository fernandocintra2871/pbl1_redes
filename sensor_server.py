from time import sleep
import socket
import threading
from sensor import *

def get_command(sensor):
    while True:
        entry = input("Digite um comando: ")
        command, value = entry.split()
        if command == "SET_TEMP":
            sensor.set_temp(int(value))
            
sensor = Sensor()

thread_command = threading.Thread(target=get_command, args=(sensor,))
thread_command.daemon = True
thread_command.start()

HOST = '127.0.0.1' 
PORT = 12345        

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.bind((HOST, PORT))

#print(f"Servidor UDP esperando na porta {PORT}...")

s.connect((HOST, PORT))

while True:
    sleep(1)
    #data, addr = s.recvfrom(1024)
    #print(f"Mensagem recebida de {addr}: {data.decode()}")

    resposta = str(sensor.get_temp())
    #s.sendall(resposta.encode())
    s. s
