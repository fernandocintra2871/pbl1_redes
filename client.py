import socket

# Define o host e a porta do servidor
HOST = '127.0.0.1'
PORT = 65432

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Conecta-se ao servidor definido
    s.connect((HOST, PORT))
    # Envia dados para o servidor
    s.sendall(b'Hello, world!')
