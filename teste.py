class Sensor:
    def __init__(self):
        self.temperatura = 0  # Inicialmente, temperatura é 0
        self.estado = False   # Inicialmente, o sensor está desligado
    
    def ligar(self):
        self.estado = True
        print("Sensor ligado.")
    
    def desligar(self):
        self.estado = False
        print("Sensor desligado.")
    
    def definir_temperatura(self, nova_temperatura):
        if self.estado:
            self.temperatura = nova_temperatura
            print(f"Temperatura definida para {self.temperatura} °C.")
        else:
            print("Erro: O sensor está desligado. Ligue o sensor primeiro.")

# Exemplo de uso da classe Sensor
if __name__ == "__main__":
    sensor = Sensor()  # Criando uma instância da classe Sensor
    
    sensor.ligar()  # Ligando o sensor
    
    sensor.definir_temperatura(25)  # Definindo a temperatura para 25 °C
    
    sensor.desligar()  # Desligando o sensor
