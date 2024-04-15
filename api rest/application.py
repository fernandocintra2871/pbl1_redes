import requests
import os
import threading
import time

color_green = "\033[92m"
color_red =  "\033[91m"
color_white = "\033[0m"
entry_detection = False

base_url = 'http://localhost:5000'

def patch_sensor(id, state):
    data = {'state': state}
    response = requests.patch(f'{base_url}/sensors/{id}', json=data)
    if response.status_code == 200:
        print('Sensor atualizado com sucesso:', response.json())
    else:
        print(f'Erro ao atualizar o sensor: {response.status_code}')


def get_sensors():
    response = requests.get(f'{base_url}/sensors')
    if response.status_code == 200:
        sensors = response.json()
        #print('Sensores: ', produtos)
        return sensors
    else:
        #print(f'Erro ao obter os sensores: {response.status_code}')
        return False

def display_sensors():
    while True:
        global entry_detection
        if not(entry_detection):
            os.system('cls')
            sensors = get_sensors()
            print(f'{"Sensor":<15}{"Estado":<15}{"Temperatura":<15}')
            for key, value in sensors.items():
                print(f'{key:<15}{color_green if value["state"] else color_red}{"Ligado" if value["state"] else "Desligado":<15}{color_white}{str(value["temperature"])+"°C":<15}')
            print("\nCommandos:\nligar [id do sensor]\ndesligar [id do sensor]\n\nPressione ENTER para digitar um comando.")
            time.sleep(1)

thread_display = threading.Thread(target=display_sensors)
thread_display.start()

while True:
    input()
    entry_detection = True
    command = input("Comando: ")
    # Execução do comando...
    entry_detection = False

    