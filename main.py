# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   Pronto Socorro - Introdução a Simulação
#   
#   Bruna Cristina Mendes
#   Flávia Santos Ribeiro
#   Luiz Eduardo Pereira    



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#                                                     ATENÇÃO !!!
#
#   Aqui serão descritos coisas a fazer:
#
#       Transfomar fila de atendimento e medicamentos em fila de prioridades
#       def inicializar_fel: Mudar em pacientes de rand para a distribuição como deveria ser  
#       def fim_chegada: Mudar em prioridade de rand para distribuição
#       def fim_chegada: Mudar em duracao_cadastro de rand para distribuição
#       def fim_cadastro: Mudar em duracao_cadastro de rand para distribuição
#       def fim_cadastro: Mudar em duracao_triagem de rand para distribuição
#       def fim_cadastro: Mudar em duracao_atendimento de rand para distribuição
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from random import randint

from Entidades.Paciente import Paciente
from Entidades.Atendente import Atendente
from Entidades.Enfermeiro import Enfermeiro
from Entidades.Medico import Medico

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

    # Gera pacientes
    # MUDAR: NUMERO DE PACIENTES É ALETORIO SEGUINDO DISTRIBUIÇÃO?
    # MUDAR: COLOCAR A DISTRIBUIÇÃO FUNCIONAR NO LUGAR DO RANDINT
    n_pacientes = 3
    tempo_chegada = []
    for i in range(n_pacientes):
        tempo_chegada.append(randint(0,100))
    tempo_chegada.sort()

    # hora é uma lista ordenada com apenas os horarios de chegada

    # Coloca um evento de 'fim_chegada' para cada paciente da simulação
    p_id = 0
    for hora in tempo_chegada:
        fel.append( (hora, 'fim_chegada', Paciente(p_id), None) )
        p_id += 1

# Dado uma tupla evento_fel, é encontrado a posição que este evento ficará na FEL seguindo sua variavel de tempo
def insere_fel(evento_fel):
    for i in range(len(fel)):
        if (evento_fel[0] < fel[i][0]):
            fel.insert(i, evento_fel)
            break

# Retorna o proximo evento da FEL
def retira_fel():
    return(fel.pop(0))

#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_CHEGADA                                                #
#                                                                                                                   #
#####################################################################################################################

def fim_chegada(evento_fel):
    # @@@ Sorteia prioridade
    evento_fel[2].prioridade = randint(1,5)
    
    # @@@ Sorteia se precisa de exame/medicamento
    boolean = randint(0, 1)
    if (boolean == 0):
        evento_fel[2].exame_medi = True
    else:
        evento_fel[2].exame_medi = False

    # @@@ Existe atendente disponivel?
    entra_fila = True
    for atendente in atendentes:
    
        # @@@ Existe atendente disponivel - SIM
        if (atendente.ocupado == False):
            entra_fila = False
            # @@@ Reserva atendente
            atendente.ocupado = True
            # @@@ Sorteia duração do cadastro
            duracao_cadastro = randint(1,5)
            # @@@ Agenda event_notice fim_cadastro
            insere_fel( (clock + duracao_cadastro, 'fim_cadastro', evento_fel[2], atendente) ) 
            break
    
    # @@@ Existe atendente disponivel - NÃO
    if (entra_fila):
        fila_cadastro.append(evento_fel[2])

#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_CADASTRO                                               #
#                                                                                                                   #
#####################################################################################################################

def fim_cadastro(evento_fel):
    # @@@ Existe paciente em aguarda cadastro?
    # @@@ Existe paciente em aguarda cadastro - SIM
    if (len(fila_cadastro) > 0):
        paciente = fila_cadastro.pop(0)
        # @@@ Sorteia duração do cadastro
        duracao_cadastro = randint(1,5)
        insere_fel( (clock + duracao_cadastro, 'fim_cadastro', paciente, evento_fel[3]) ) 
    # @@@ Existe paciente em aguarda cadastro - NÃO
    else:
        # @@@ Libera atendente
        evento_fel[3].ocupado = False

    # @@@ A prioridade é emergencia (5)?
    # @@@ A prioridade é emergencia (5) - SIM
    if (evento_fel[2].prioridade == 5):

        # @@@ Existe medico ocioso?
        entra_fila = True
        for medico in medicos:

            # @@@ Existe medico ocioso - SIM
            if (medico.ocupado == False):
                entra_fila = False
                # @@@ Reserva medico
                medico.ocupado = True
                # @@@ Sorteia duração do atendimento
                duracao_atendimento = randint(1,5)
                # @@@ Agenda event_notice fim_atendimento
                insere_fel( (clock + duracao_atendimento, 'fim_atendimento', evento_fel[2], medico) ) 
                break

        # @@@ Existe medico ocioso - NÃO
        if (entra_fila):
            fila_atendimento.append(evento_fel[2])
    
    # @@@ A prioridade é emergencia (5) - NÃO
    else:
        # @@@ Existe enfermeiro ocioso?
        entra_fila = True
        for enfermeiro in enfermeiros:

            # @@@ Existe enfermeiro ocioso - SIM
            if (enfermeiro.ocupado == False):
                entra_fila = False
                # @@@ Reserva enfermeiro
                enfermeiro.ocupado = True
                # @@@ Sorteia duração da triagem
                duracao_triagem = randint(1,5)
                # @@@ Agenda event_notice fim_triagem
                insere_fel( (clock + duracao_triagem, 'fim_triagem', evento_fel[2], enfermeiro) ) 
                break

        # @@@ Existe enfermeiro ocioso - NÃO
        if (entra_fila):
            fila_triagem.append(evento_fel[2])


#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_TRIAGEM                                                #
#                                                                                                                   #
#####################################################################################################################

def fim_triagem(evento_fel):
    pass

#####################################################################################################################
#                                                                                                                   #
#                                               EVENTO FIM_ATENDIMENTO                                              #
#                                                                                                                   #
#####################################################################################################################

def fim_atendimento(evento_fel):
    pass

#####################################################################################################################
#                                                                                                                   #
#                                           EVENTO FIM_MEDICAMENTOS E EXAMES                                        #
#                                                                                                                   #
#####################################################################################################################

def fim_medicamentosexames(evento_fel):
    pass

#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

#####################################################
#                                                   #
#                   PARAMETROS                      #
#                                                   #
#####################################################

fel = [] # Lista temporal de atividades
clock = 0 # Clock do tempo atual
clock_anterior = 0 # Clock da ultima mudança de tempo
executa_fel = {'fim_chegada': fim_chegada, 'fim_cadastro': fim_cadastro, 'fim_triagem': fim_triagem, 'fim_atendimento': fim_atendimento, 'fim_medicamentosexames': fim_medicamentosexames}

atendentes = []
enfermeiros = []
medicos = []
fila_cadastro = []
fila_triagem = []
fila_atendimento = []
fila_medicamentosexames = []

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

#####################################################
#                                                   #
#                    EXECUÇÃO                       #
#                                                   #
#####################################################

le_arquivo('entrada.txt')
inicializa_fel()

for i in range(ATD):
    atendentes.append(Atendente(i))
for i in range(ENF):
    enfermeiros.append(Enfermeiro(i))
for i in range(MED):
    medicos.append(Medico(i))

# Enquanto tiver eventos na FEL, a simulação continua

while (len(fel) > 0):
    print()
    print(fel)

    evento_fel = retira_fel()
    
    # Se o tempo mudou, então guarda a hora do ultimo clock, ( * ?PRECISA DISSO? * ) 
    if (evento_fel[1] != clock):
        clock_anterior = clock
    clock = evento_fel[0]
        
    # O nome função no qual se deve executar esta contida em evento_fel[1], e o executa_fel redireciona para a função correta.
    executa_fel[evento_fel[1]](evento_fel)