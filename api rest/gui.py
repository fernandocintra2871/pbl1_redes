import tkinter as tk
from tkinter import ttk
import random

class Sensor:
    def __init__(self, name):
        self.name = name
        self.state = False  # False significa desligado, True significa ligado
        self.temperature = random.uniform(15, 30)  # Temperatura inicial aleatória entre 15 e 30ºC

    def toggle_state(self):
        self.state = not self.state

    def update_temperature(self):
        if self.state:
            # Se o sensor está ligado, atualiza a temperatura para um valor aleatório entre 15 e 30ºC
            self.temperature = random.uniform(15, 30)

    def __str__(self):
        state_str = "Ligado" if self.state else "Desligado"
        return f"{self.name}: {state_str} - {self.temperature:.2f}ºC"

class SensorGUI(tk.Tk):
    def __init__(self, sensors):
        super().__init__()
        self.title("Estado dos Sensores")

        # Crie uma lista de sensores
        self.sensors = sensors
        
        # Adicione um frame para organizar os widgets
        self.frame = tk.Frame(self)
        self.frame.pack()

        # Adicione um rótulo e um botão para cada sensor
        self.sensor_labels = []
        self.sensor_buttons = []
        
        for sensor in self.sensors:
            label = ttk.Label(self.frame, text=str(sensor))
            label.pack()

            button = ttk.Button(self.frame, text=f"Ligar/Desligar {sensor.name}",
                                command=lambda s=sensor, l=label: self.toggle_sensor(s, l))
            button.pack()

            self.sensor_labels.append(label)
            self.sensor_buttons.append(button)

        # Inicia a atualização periódica da temperatura
        self.update_temperature()

    def toggle_sensor(self, sensor, label):
        # Altera o estado do sensor
        sensor.toggle_state()
        # Atualiza o rótulo para refletir o novo estado e a temperatura
        label.config(text=str(sensor))

    def update_temperature(self):
        # Atualiza a temperatura de cada sensor se estiver ligado
        for i, sensor in enumerate(self.sensors):
            sensor.update_temperature()
            # Atualiza o rótulo correspondente para exibir a nova temperatura
            self.sensor_labels[i].config(text=str(sensor))

        # Agenda a próxima atualização em 1000 ms (1 segundo)
        self.after(1000, self.update_temperature)

def main():
    # Cria três sensores com nomes diferentes
    sensors = [Sensor("Sensor 1"), Sensor("Sensor 2"), Sensor("Sensor 3")]

    # Cria e executa a interface gráfica
    gui = SensorGUI(sensors)
    gui.mainloop()

if __name__ == "__main__":
    main()
