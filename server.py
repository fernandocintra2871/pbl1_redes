import socket

# Define o host e a porta em que o servidor irá ouvir
HOST = '127.0.0.1'
PORT = 65432

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Liga o socket ao host e porta definidos
    s.bind((HOST, PORT))
    # Faz o servidor ouvir conexões
    s.listen()
    print("Aguardando conexão...")
    # Aceita a conexão e obtém o objeto de socket e o endereço do cliente
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            # Recebe os dados enviados pelo cliente
            data = conn.recv(1024)
            if not data:
                break
            # Exibe os dados recebidos
            print('Dados recebidos:', data.decode())
