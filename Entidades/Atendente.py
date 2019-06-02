class Atendente:

    def __init__(self,id):
        self.id = id
        self.total_ocioso = 0.0
        self.inicio_horario_ocioso = 0.0
        self.ocupado = False
        self.evento_atual = None #ponteiro

    # Quando alocar para uma ação, olhar horario atual e o horario em que começou a ficar ocioso 
    def set_tempo_ocioso(self, horario_atual):
        self.total_ocioso += horario_atual - self.inicio_horario_ocioso
        return
