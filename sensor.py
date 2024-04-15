class Sensor:
    def __init__(self):
        self.temp = 0
        self.state = False
    
    def get_temp(self):
        return self.temp

    def set_temp(self, temp):
        self.temp = temp

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state