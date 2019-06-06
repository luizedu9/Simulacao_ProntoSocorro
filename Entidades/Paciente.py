class Paciente:

    def __init__(self,id):
        self.id = id
        self.prioridade = 0
        self.exame_medi = False
        self.clock = 0.0
        self.tempo_fila_cadastro = 0.0
        self.tempo_fila_triagem = 0.0
        self.tempo_fila_atendimento = 0.0
        self.tempo_fila_medicamento = 0.0

    def tempo_fila_total(self):
        return(self.tempo_fila_cadastro + self.tempo_fila_triagem + self.tempo_fila_atendimento + self.tempo_fila_medicamento)
