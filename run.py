# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   Pronto Socorro - Introdução a Simulação
#   
#   Bruna Cristina Mendes
#   Flávia Santos Ribeiro
#   Luiz Eduardo Pereira 

import os
import sys

try:
    kpi_ociosidade = sys.argv[1]
    kpi_tempo = sys.argv[2]
    kpi_tamanho = sys.argv[3]
except:
    print("ERRO - PARAMETROS DE KPI ESPERADOS (OCIOSIDADE, TEMPO, TAMANHO) ")
    print("OCIOSIDADE: atendente / enfermeiro / medico")
    print("TEMPO: cadastro, triagem, atendimento, medicamento")
    print("TAMANHO: cadastro, triagem, atendimento, medicamento")
    exit()

with open('resultados.csv', 'w') as file:
    file.write('Ociosidade ' + kpi_ociosidade + '\tTemp. Med. ' + kpi_tempo + '\tTam. Med. ' + kpi_tamanho + '\n')

for i in range(100):
    os.system('python3 -B main.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3])