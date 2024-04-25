import requests
import os
import threading
import time

color_green = "\033[92m"
color_red =  "\033[91m"
color_white = "\033[0m"
entry_detection = False

base_url = 'http://172.16.103.9:12345'

def post_command(command, sensor):
    dados = {'command': command, 'sensor': sensor}
    response = requests.post(f'{base_url}/commands', json=dados)
    if response.status_code == 201:
        print('Comando adicionado com sucesso:', response.json())
    else:
        print(f'Erro ao adicionar o comando: {response.status_code}')

def get_sensors():
    response = requests.get(f'{base_url}/sensors')
    if response.status_code == 200:
        sensors = response.json()
        #print('Sensores: ', produtos)
        return sensors
    else:
        #print(f'Erro ao obter os sensores: {response.status_code}')
        return False

def clear_console():
    # Verifica o sistema operacional e executa o comando apropriado
    if os.name == "posix":  # Linux e macOS
        os.system("clear")
    elif os.name == "nt":   # Windows
        os.system("cls")
    else:  # Outros sistemas, pode não funcionar corretamente
        print("Não foi possível limpar a tela para este sistema.")

def display_sensors():
    while True:
        global entry_detection
        if not(entry_detection):
            clear_console()
            sensors = get_sensors()
            print(f'{"Sensor":<15}{"Estado":<15}{"Temperatura":<15}')
            key = 0
            for value in sensors:
                print(f'{key:<15}{color_green if value["state"] else color_red}{"Ligado" if value["state"] else "Desligado":<15}{color_white}{str(value["temp"])+"°C":<15}')
                key += 1
            print("\nCommandos:\nligar [id do sensor]\ndesligar [id do sensor]\n\nPressione ENTER para digitar um comando.")
            time.sleep(3)

thread_display = threading.Thread(target=display_sensors)
thread_display.daemon = True
thread_display.start()

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
            if sensor_id >= 0 and sensor_id < len(sensors):
                if command == "ligar":
                    if sensors[sensor_id]["state"] != True:
                        post_command(command, sensor_id)
                    else:
                        print('\nO sensor já está ligado!')
                        time.sleep(3)
                elif command == "desligar":
                    if sensors[sensor_id]["state"] != False:
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

    