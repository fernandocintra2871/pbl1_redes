import socket
import threading

class Broker:
    def __init__(self):
        self.messages = []

    def start(self):
        # Inicia o servidor em uma thread separada
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def run_server(self):
        # Configura o servidor para ouvir conexões
        host = 'localhost'
        port = 12345
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)

        print("Broker aguardando conexões...")

        while True:
            # Aceita conexões dos clientes
            client_socket, addr = server_socket.accept()
            print('Conectado por', addr)
            # Inicia uma thread para lidar com o cliente
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            # Recebe dados do cliente
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            # Armazena a mensagem recebida
            self.messages.append(message)
            print("Mensagem recebida:", message)
        # Fecha a conexão com o cliente
        client_socket.close()

    def send_message(self, message):
        # Envie a mensagem para todos os clientes conectados
        for client_socket in self.client_sockets:
            client_socket.send(message.encode())

# Exemplo de uso do broker
if __name__ == "__main__":
    broker = Broker()
    broker.start()
