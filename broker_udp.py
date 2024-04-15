import socket

HOST = '127.0.0.1'
PORT = 12345  

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print(f"Servidor UDP esperando na porta {PORT}...")

while True:
    data, addr = s.recvfrom(1024)
    print(f"Mensagem recebida de {addr}: {data.decode()}")