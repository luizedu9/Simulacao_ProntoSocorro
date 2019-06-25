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
    entrada = sys.argv[1]
    saida = sys.argv[2]
except:
    print("ERRO - PARAMETROS")
    print("python3 -B run.py entrada.txt saida.csv")
    exit()

with open(saida, 'w') as file:
    file.write('OG\tOA\tOE\tOM\tTeG\tTeP1\tTeP2\tTeP3\tTeP4\tTeP5\tTeMFC\tTeMFT\tTeMFA\tTeMFM\tTaG\tTaMFC\tTaMFT\tTaMFA\tTaMFM\n')

for i in range(100):
    print(str(i+1) + 'ª Simulação')
    os.system('python3 -B main.py ' + sys.argv[1] + ' ' + sys.argv[2])