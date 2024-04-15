import socket

# Define o host e a porta do servidor
HOST = '127.0.0.1'
PORT = 12345

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Conecta-se ao servidor definido
    s.connect((HOST, PORT))
    # Envia dados para o servidor
    command = input("Digite o comando: ")
    s.sendall(command.encode())

    data, addr = s.recvfrom(1024)
    print(f"Mensagem recebida de {addr}: {data.decode()}")