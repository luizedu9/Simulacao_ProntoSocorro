# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   Pronto Socorro - Introdução a Simulação
#   
#   Bruna Cristina Mendes
#   Flávia Santos Ribeiro
#   Luiz Eduardo Pereira  

class Medico:

    def __init__(self, id):
        self.id = id
        self.total_ocioso = 0.0
        self.inicio_horario_ocioso = 0.0
        self.ocupado = False
        self.cargo = 'Medico'

    # Quando alocar para uma ação, olhar horario atual e o horario em que começou a ficar ocioso 
    def set_tempo_ocioso(self, clock):
        self.total_ocioso += clock - self.inicio_horario_ocioso
        return

    # Se foi liberado, quer dizer que se deu inicio ao tempo ocioso, então libera e guarda o inicio do tempo ocioso 
    def libera(self, clock):
        self.ocupado = False
        self.inicio_horario_ocioso = clock

    # Se foi reservado, quer dizer que ele estava ocioso, então reserva e conta o tempo ocioso
    def reserva(self, clock):
        self.ocupado = True
        self.set_tempo_ocioso(clock)