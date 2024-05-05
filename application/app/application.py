import requests
import os
import threading
import time

HOST = os.environ.get("ip_broker") # Pega o IP do broker passado como váriavel de ambiente Docker

# Tags de cores usada para mudar a cor dos caracteres no terminal
color_green = "\033[92m"
color_red =  "\033[91m"
color_white = "\033[0m"
entry_detection = False

# API
base_url = 'http://'+HOST+':12345'

# Metodo POST para enviar comandos para o Broker
def post_command(command, sensor):
    dados = {'command': command, 'sensor': sensor}
    response = requests.post(f'{base_url}/commands', json=dados)
    if response.status_code == 201:
        print('Comando adicionado com sucesso:', response.json())
    else:
        print(f'Erro ao adicionar o comando: {response.status_code}')

# Metodo GET usado para pegar os dados de todos os sensores conectados ao Broker
def get_sensors():
    response = requests.get(f'{base_url}/sensors')
    if response.status_code == 200:
        sensors = response.json()
        return sensors
    else:
        return False

# Limpa o console
def clear_console():
    # Verifica o sistema operacional e executa o comando apropriado
    if os.name == "posix": # Linux e macOS
        os.system("clear")
    elif os.name == "nt": # Windows
        os.system("cls")
    else:
        print("Não foi possível limpar a tela para este sistema.")

# Exbibe os dados Estado e Temperatura de cada sensor no terminal
def display_sensors():
    while True:
        global entry_detection
        if not(entry_detection):
            while True: # Fica em loop até se conectar ao Broker
                clear_console()
                try:
                    sensors = get_sensors()
                except requests.exceptions.RequestException: # Caso a Aplicação não consiga pedir dados ao Broker começa a tentar reconexão
                    print("\nTentando conexão com o Broker...")
                    time.sleep(3)
                else:
                    break
            print(f'{"Sensor":<15}{"Estado":<15}{"Temperatura":<15}')
            key = 0
            for key, value in sensors.items():
                print(f'{key:<15}{color_green if value["state"] else color_red}{"Ligado" if value["state"] else "Desligado":<15}{color_white}{str(value["temp"])+"°C":<15}')
            print("\nCommandos:\nligar [id do sensor]\ndesligar [id do sensor]\n\nPressione ENTER para digitar um comando.")
            time.sleep(3)


# Cria uma thread pra ficar exibindo os dados atualizados no terminal
thread_display = threading.Thread(target=display_sensors)
thread_display.daemon = True
thread_display.start()

# Verifica a entrada de comandos dos usuario
while True:
    input()
    entry_detection = True
    command = input("Comando: ")
    command_list = command.split()
    if len(command_list) == 2:
        command = command_list[0]
        sensor_id = int(command_list[1])
        sensors = get_sensors()
        if command in ['ligar', 'desligar']:
            if str(sensor_id) in sensors.keys():
                if command == "ligar":
                    print(sensors)
                    if sensors[str(sensor_id)]["state"] != True:
                        post_command(command, sensor_id)
                    else:
                        print('\nO sensor já está ligado!')
                        time.sleep(3)
                elif command == "desligar":
                    if sensors[str(sensor_id)]["state"] != False:
                        post_command(command, sensor_id)
                    else:
                        print('\nO sensor já está desligado!')
                        time.sleep(3)
            else:
                print('\nSensor inexistente!')
                time.sleep(3)
        else:
            print('\nComando inexistente!')
            time.sleep(3)
    entry_detection = False

    