# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   Pronto Socorro - Introdução a Simulação
#   
#   Bruna Cristina Mendes
#   Flávia Santos Ribeiro
#   Luiz Eduardo Pereira    

#####################################################################################################################
#                                                                                                                   #
#                                                        ARQUIVO                                                    #
#                                                                                                                   #
#####################################################################################################################

def le_arquivo(nome):

    global TTS, PRO, MED,ENF, ATD, PRI, CHE, CAD,TRI, ATE, EXA

    with open(nome) as arq:
        for linha in arq:
            linha = linha.split(' ')
            if linha[0] == 'T':
                if linha[1] == 'TTS':
                    TTS = int(linha[2])
                elif linha[1] == 'CHE':
                    CHE = (linha[2],float(linha[3]),float(linha[4]),float(linha[5]))
                elif linha[1] == 'CAD':
                    CAD = (linha[2],float(linha[3]),float(linha[4]),float(linha[5]))
                elif linha[1] == 'TRI':
                    TRI = (linha[2],float(linha[3]),float(linha[4]),float(linha[5]))
                elif linha[1] == 'ATE':
                    ATE =(linha[2],float(linha[3]),float(linha[4]),float(linha[5]))
                elif linha[1] == 'EXA':
                    EXA =(linha[2],float(linha[3]),float(linha[4]),float(linha[5]))
            elif linha[0] == 'P':
                if linha[1] == 'PRO':
                    PRO = int(linha[2])
                elif linha[1] == 'PRI':
                    PRI = (int(linha[2]),int(linha[3]), int(linha[4]), int(linha[5]), int(linha[6]))
            elif linha[0] == 'Q':
                if linha[1] == 'MED':
                    MED = int(linha[2])
                elif linha[1] == 'ENF':
                    ENF = int(linha[2])
                elif linha[1] == 'ATD':
                    ATD = int(linha[2])
            else:
                pass
    
# Essa função inicializa todos os fatores aleatorios, como horario de chegada dos pacientes, etc
def inicializar():
    le_arquivo('entrada.txt')
    print(TTS,' ',PRO, ' ',PRI,' ',MED,' ',ENF, ' ',ATD,' ',CHE,' ', CAD,' ',TRI,' ',ATE,' ',EXA)
    pass

#####################################################################################################################
#                                                                                                                   #
#                                                         FEL                                                       #
#                                                                                                                   #
#####################################################################################################################

#
# EVENTO_FEL: (0 Tempo, 1 Event_Listener, 2 Paciente, 3 Funcionario)
#

# Essa função inicializa a FEL com os event listeners da chegada dos pacientes
def inicializa_fel():

    # FAZ A DISTRIBUIÇÃO E DESCOBRE A CHEGADA DOS PACIENTES ***************************
    # SUPONTO Q ELES CHEGAM EM UMA LISTA ORDENANA, COLOCA NA FEL **********************

    # chegada_pacientes é uma lista ordenada com apenas os horarios de chegada

    # Coloca um evento de 'fim_chegada' para cada paciente da simulação
    p_id = 0
    for chegada_paciente in chegada_pacientes:
        fel.append( (chegada_paciente, 'fim_chegada', p_id, None) )
        p_id += 1
    return

# Dado uma tupla evento_fel, é encontrado a posição que este evento ficará na FEL seguindo sua variavel de tempo
def insere_fel(evento_fel):
    for i in range(len(fel)):
        if (evento_fel[0] < fel[i][1]):
            fel.insert(i, evento_fel[0])
            break
    return

# Retorna o proximo evento da FEL
def retira_fel():
    return(fel.pop(0))

#####################################################################################################################
#                                                                                                                   #
#                                                       PARAMETROS                                                  #
#                                                                                                                   #
#####################################################################################################################

fel = [] # Lista temporal de atividades
clock = 0 # Clock do tempo atual
fel_dict = {'fim_chegada': fim_chegada, 'fim_cadastro': fim_cadastro, 'fim_triagem': fim_triagem, 'fim_atendimento': fim_atendimento, 'fim_medicamentosexames': fim_medicamentosexames}

TTS = 0 # tempo maximo de simulacao em minutos
PRO = 0 # probabilidade de necessidade de exames/medicamentos
PRI = (0,0,0,0,0) # probabilidade da prioridade de atendimento dos pacientes
MED = 0 # quatidade de medicos
ENF = 0 # quantidade de enfermeiros
ATD = 0 # quantidade de atendentes
CHE =('',0.0,0.0,0.0) # distribuicao chegada_paciente
CAD =('',0.0,0.0,0.0) # distribuicao cadastro_paciente
TRI =('',0.0,0.0,0.0) # distribuicao triagem
ATE =('',0.0,0.0,0.0) # distribuicao atendimento
EXA =('',0.0,0.0,0.0) # distribuicao exames/medicamentos
prioridade_enfermeiro_triagem = 80 # probabilidade da prioridade ser triagem
prioridade_enfermeiro_medicamentos = 20 # probabilidade da prioridade ser medicamento

#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

inicializar()
inicializa_fel()

# Enquanto tiver eventos na FEL, a simulação continua
while (len(fel) > 0):
    evento_fel = retira_fel()

    # FAZ COISAS ***************