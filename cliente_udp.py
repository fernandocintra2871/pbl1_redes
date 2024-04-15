import socket

# Configurações do servidor UDP
SERVER_HOST = '127.0.0.1'  # Endereço IP do servidor
SERVER_PORT = 12345        # Porta do servidor

# Tamanho máximo dos dados recebidos
MAX_BYTES = 1024


# Criando um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket localmente para receber mensagens do servidor
client_socket.bind(('127.0.0.1', 0))
local_port = client_socket.getsockname()[1]
print(f"Cliente UDP aguardando mensagens na porta {local_port}...")

# Conectando-se ao servidor UDP
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Loop principal para receber mensagens do servidor
while True:
    # Recebendo dados do servidor
    data, server_address = client_socket.recvfrom(MAX_BYTES)
    print(f"Mensagem recebida do servidor ({server_address}): {data.decode()}")
