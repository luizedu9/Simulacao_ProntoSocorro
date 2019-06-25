# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   Pronto Socorro - Introdução a Simulação
#   
#   Bruna Cristina Mendes
#   Flávia Santos Ribeiro
#   Luiz Eduardo Pereira    

from random import randint
import random
import numpy as np
import sys

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

    global TTS, PRO, MED, ENF, ATD, PRI, CHE, CAD, TRI, ATE, EXA

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
                    PRO = float(linha[2])
                elif linha[1] == 'PRI':
                    PRI = [int(linha[2]),int(linha[3]), int(linha[4]), int(linha[5]), int(linha[6])]
                    PRI[1] = PRI[0] + PRI[1]
                    PRI[2] = PRI[1] + PRI[2]
                    PRI[3] = PRI[2] + PRI[3]
                    PRI[4] = PRI[3] + PRI[4]
                    PRI = (PRI[0], PRI[1], PRI[2], PRI[3], PRI[4])
            elif linha[0] == 'Q':
                if linha[1] == 'MED':
                    MED = int(linha[2])
                elif linha[1] == 'ENF':
                    ENF = int(linha[2])
                elif linha[1] == 'ATD':
                    ATD = int(linha[2])

#####################################################################################################################
#                                                                                                                   #
#                                             SORTEIA DURAÇÃO DOS EVENTOS                                           #
#                                                                                                                   #
#####################################################################################################################
def duracao_evento(distribuicao):

    if distribuicao[0] == 'EXP':
        vetor = np.random.exponential(1/distribuicao[1], 1)
        return round(float(vetor),2)

    if distribuicao[0] == 'NOR':
        x = np.random.normal(distribuicao[1], distribuicao[2], 1)# [1] eh media, [2] eh desvio padrao
        x = round(float(x),2)
        return x

    if distribuicao[0] == 'TRI':
        x = np.random.triangular(distribuicao[1], distribuicao[2], distribuicao[3], 1)
        x = round(float(x),2)
        return x

    if distribuicao[0] == 'UNI':
        x = np.random.uniform(distribuicao[1],distribuicao[2],1)
        x = round(float(x),2)
        return x

    if distribuicao[0] == 'BET':
        vetor = np.random.beta(distribuicao[1],distribuicao[2], 1)
        return round(float(vetor),2)

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

    global CHE, TTS

    hora_chegada = [0] #vetor com horarios
    for i in range(TTS-1):
        if i<TTS:
            chegada_atual = duracao_evento(CHE)
            hora_chegada.append(hora_chegada[-1] + chegada_atual)
            if hora_chegada[-1] > TTS:
                hora_chegada.pop()
            i = i + hora_chegada[-1] + chegada_atual
    hora_chegada.sort()
    del(hora_chegada[0])

    # hora é uma lista ordenada com apenas os horarios de chegada

    # Coloca um evento de 'fim_chegada' para cada paciente da simulação
    p_id = 0
    for hora in hora_chegada:
        pacientes.append(Paciente(p_id))
        fel.append((hora, 'fim_chegada', pacientes[p_id], None))
        p_id += 1

# Dado uma tupla evento_fel, é encontrado a posição que este evento ficará na FEL seguindo sua variavel de tempo
def insere_fel(evento_fel):
    inseriu = False
    for i in range(len(fel)):
            if evento_fel[0] < fel[i][0]:
                fel.insert(i, evento_fel)
                inseriu = True
                break
    if not(inseriu):
        fel.append(evento_fel)

# Retorna o proximo evento da FEL
def retira_fel():
    return(fel.pop(0))

#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_CHEGADA                                                #
#                                                                                                                   #
#####################################################################################################################

def fim_chegada(evento_fel):

    global CAD
    # @@@ Sorteia prioridade
    pri = randint(0,100)
    if pri <= PRI[0]:
        evento_fel[2].prioridade = 1
    elif pri <= PRI[1]:
        evento_fel[2].prioridade = 2
    elif pri <= PRI[2]:
        evento_fel[2].prioridade = 3
    elif pri <= PRI[3]:
        evento_fel[2].prioridade = 4
    elif pri <= PRI[4]:
        evento_fel[2].prioridade = 5

    # @@@ Sorteia se precisa de exame/medicamento
    chance = random.random()
    if (chance <= PRO):
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
            atendente.reserva(clock)
            # @@@ Sorteia duração do cadastro
            duracao_cadastro = duracao_evento(CAD)
            # @@@ Agenda event_notice fim_cadastro
            insere_fel((clock + duracao_cadastro, 'fim_cadastro', evento_fel[2], atendente))
            break
    
    # @@@ Existe atendente disponivel - NÃO
    if (entra_fila):
        # @@@ Coloca paciente na fila de cadastro
        insere_fila_cadastro(fila_cadastro, evento_fel[2])
        # Tempo que paciente entrou na fila
        evento_fel[2].tempo_entrou_fila_cadastro = clock

#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_CADASTRO                                               #
#                                                                                                                   #
#####################################################################################################################

def fim_cadastro(evento_fel):

    global CAD, TRI, ATE
    # @@@ Existe paciente em aguarda cadastro?
    # @@@ Existe paciente em aguarda cadastro - SIM
    if len(fila_cadastro) > 0:
        paciente = fila_cadastro.pop(0)
        # Calcula tempo em que paciente ficou na fila
        paciente.tempo_fila_cadastro = clock - paciente.tempo_entrou_fila_cadastro
        #print('Paciente ' + str(paciente.id) + ' saiu da fila cadastro no tempo ' + str(clock))
        # @@@ Sorteia duração do cadastro
        duracao_cadastro = duracao_evento(CAD)
        # @@@ Agenda event_notice fim_cadastro
        insere_fel((clock + duracao_cadastro, 'fim_cadastro', paciente, evento_fel[3]))
    # @@@ Existe paciente em aguarda cadastro - NÃO
    else:
        # @@@ Libera atendente
        evento_fel[3].libera(clock)

    # @@@ A prioridade é emergencia (5)?
    # @@@ A prioridade é emergencia (5) - SIM
    if evento_fel[2].prioridade == 5:

        # @@@ Existe medico ocioso?
        entra_fila = True
        for medico in medicos:

            # @@@ Existe medico ocioso - SIM
            if medico.ocupado == False:
                entra_fila = False
                # @@@ Reserva medico
                medico.reserva(clock)
                # @@@ Sorteia duração do atendimento
                duracao_atendimento = duracao_evento(ATE)
                # @@@ Agenda event_notice fim_atendimento
                insere_fel((clock + duracao_atendimento, 'fim_atendimento', evento_fel[2], medico))
                break

        # @@@ Existe medico ocioso - NÃO
        if (entra_fila):
            # @@@ Coloca paciente na fila de atendimento
            insere_fila_prioridade(fila_atendimento, evento_fel[2])
            # Tempo que paciente entrou na fila
            evento_fel[2].tempo_entrou_fila_atendimento = clock
    
    # @@@ A prioridade é emergencia (5) - NÃO
    else:
        # @@@ Existe enfermeiro ocioso?
        entra_fila = True
        for enfermeiro in enfermeiros:

            # @@@ Existe enfermeiro ocioso - SIM
            if (enfermeiro.ocupado == False):
                entra_fila = False
                # @@@ Reserva enfermeiro
                enfermeiro.reserva(clock)
                # @@@ Sorteia duração da triagem
                duracao_triagem = duracao_evento(TRI)
                # @@@ Agenda event_notice fim_triagem
                insere_fel((clock + duracao_triagem, 'fim_triagem', evento_fel[2], enfermeiro))
                break

        # @@@ Existe enfermeiro ocioso - NÃO
        if (entra_fila):
            # @@@ Coloca paciente na fila de triagem
            fila_triagem.append(evento_fel[2])
            # Tempo que paciente entrou na fila
            evento_fel[2].tempo_entrou_fila_triagem = clock


#####################################################################################################################
#                                                                                                                   #
#                                                 EVENTO FIM_TRIAGEM                                                #
#                                                                                                                   #
#####################################################################################################################

def fim_triagem(evento_fel):

    global TRI, EXA,ATE

    # @@@ Existe paciente aguardando triagem e medicamento?
    # @@@ Existe paciente aguardando triagem e medicamento - SIM
    if (len(fila_triagem) > 0 and len(fila_medicamentosexames) > 0):
        # @@@ Sorteia se enfermeiro irá para triagem
        if (randint(0, 100) < prioridade_triagem):
            paciente = fila_triagem.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_triagem = clock - paciente.tempo_entrou_fila_triagem
            # @@@ Sorteia duração da triagem
            duracao_triagem = duracao_evento(TRI)
            # @@@ Agenda event_notice fim_triagem
            insere_fel((clock + duracao_triagem, 'fim_triagem', paciente, evento_fel[3]))
        # @@@ Sorteia se enfermeiro irá para medicamento
        else:
            paciente = fila_medicamentosexames.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_medicamento = clock - paciente.tempo_entrou_fila_medicamento
            # @@@ Sorteia duração dos exames/medicamentos
            duracao_medicamentoexames = duracao_evento(EXA)
            # @@@ Agenda event_notice fim_medicamentosexames
            insere_fel((clock + duracao_medicamentoexames, 'fim_medicamentosexames', paciente, evento_fel[3]))
    # @@@ Existe paciente aguardando triagem e medicamento - NÃO
    else:
        # @@@ Existe paciente aguardando triagem?
        # @@@ Existe paciente aguardando triagem - SIM
        if len(fila_triagem) > 0:
            paciente = fila_triagem.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_triagem = clock - paciente.tempo_entrou_fila_triagem
            # @@@ Sorteia duração da triagem
            duracao_triagem = duracao_evento(TRI)
            # @@@ Agenda event_notice fim_triagem
            insere_fel((clock + duracao_triagem, 'fim_triagem', paciente, evento_fel[3]))
        # @@@ Existe paciente aguardando triagem - NÃO
        else:
            # @@@ Existe paciente aguardando exames/medicamento?
            # @@@ Existe paciente aguardando exames/medicamento - SIM
            if len(fila_medicamentosexames) > 0:
                paciente = fila_medicamentosexames.pop(0)
                # Calcula tempo em que paciente ficou na fila
                paciente.tempo_fila_medicamento = clock - paciente.tempo_entrou_fila_medicamento
                # @@@ Sorteia duração dos exames/medicamentos
                duracao_medicamentoexames = duracao_evento(EXA)
                # @@@ Agenda event_notice fim_medicamentosexames
                insere_fel((clock + duracao_medicamentoexames, 'fim_medicamentosexames', paciente, evento_fel[3]))
            # @@@ Existe paciente aguardando exames/medicamento - NÃO
            else:
                # @@@ Libera enfermerio
                evento_fel[3].libera(clock)

    # @@@ Existe medico disponivel?
    entra_fila = True
    for medico in medicos:

        # @@@ Existe medico disponivel - SIM
        if medico.ocupado == False:
            entra_fila = False
            # @@@ Reserva medico
            medico.reserva(clock)
            # @@@ Sorteia duração do atendimento
            duracao_atendimento = duracao_evento(ATE)
            # @@@ Agenda event_notice fim_atendimento
            insere_fel((clock + duracao_atendimento, 'fim_atendimento', evento_fel[2], medico))
            break
    
    # @@@ Existe medico disponivel - NÃO
    if (entra_fila):
        # @@@ Coloca paciente na fila de atendimento
        insere_fila_prioridade(fila_atendimento, evento_fel[2])
        # Tempo que paciente entrou na fila
        evento_fel[2].tempo_entrou_fila_atendimento = clock

#####################################################################################################################
#                                                                                                                   #
#                                               EVENTO FIM_ATENDIMENTO                                              #
#                                                                                                                   #
#####################################################################################################################

def fim_atendimento(evento_fel):

    global ATE, EXA
    # @@@ Existe paciente aguardando atendimento?
    # @@@ Existe paciente aguardando atendimento - SIM
    if len(fila_atendimento) > 0:
        paciente = fila_atendimento.pop(0)
        # Calcula tempo em que paciente ficou na fila
        paciente.tempo_fila_atendimento = clock - paciente.tempo_entrou_fila_atendimento
        # @@@ Sorteia duração do atendimento
        duracao_atendimento = duracao_evento(ATE)
        # @@@ Agenda event_notice fim_atendimento
        insere_fel((clock + duracao_atendimento, 'fim_atendimento', paciente, evento_fel[3]))
    # @@@ Existe paciente aguardando atendimento - NÃO
    else:
        # @@@ Libera Medico
        evento_fel[3].libera(clock)

    # @@@ Paciente precisa de medicamentos/exame?
    # @@@ Paciente precisa de medicamentos/exame - SIM
    if (evento_fel[2].exame_medi):
        # @@@ Existe enfermeiro ocioso?
        entra_fila = True
        for enfermeiro in enfermeiros:

            # @@@ Existe enfermeiro ocioso - SIM
            if enfermeiro.ocupado == False:
                entra_fila = False
                # @@@ Reserva enfermeiro
                enfermeiro.reserva(clock)
                # @@@ Sorteia duração dos medicamentos/exames
                duracao_medicamentoexames = duracao_evento(EXA)
                # @@@ Agenda event_notice fim_medicamentosexames
                insere_fel((clock + duracao_medicamentoexames, 'fim_medicamentosexames', evento_fel[2], enfermeiro))
                break

        # @@@ Existe enfermeiro ocioso - NÃO
        if (entra_fila):
            # @@@ Coloca paciente na fila de exames/medicamentos
            insere_fila_prioridade(fila_medicamentosexames, evento_fel[2])
            # Tempo que paciente entrou na fila
            evento_fel[2].tempo_entrou_fila_medicamento = clock

    # @@@ Paciente precisa de medicamentos/exame - NÃO
    else:
        # @@@ Libera paciente
        pass

#####################################################################################################################
#                                                                                                                   #
#                                           EVENTO FIM_MEDICAMENTOS E EXAMES                                        #
#                                                                                                                   #
#####################################################################################################################

def fim_medicamentosexames(evento_fel):

    global EXA, TRI
    
    # @@@ Existe paciente aguardando triagem e medicamento?
    # @@@ Existe paciente aguardando triagem e medicamento - SIM
    if (len(fila_triagem) > 0 and len(fila_medicamentosexames) > 0):
        # @@@ Sorteia se enfermeiro irá para triagem
        if (randint(0, 100) < prioridade_triagem):
            paciente = fila_triagem.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_triagem = clock - paciente.tempo_entrou_fila_triagem
            # @@@ Sorteia duração da triagem
            duracao_triagem = duracao_evento(TRI)
            # @@@ Agenda event_notice fim_triagem
            insere_fel((clock + duracao_triagem, 'fim_triagem', paciente, evento_fel[3]))
        # @@@ Sorteia se enfermeiro irá para medicamento
        else:
            paciente = fila_medicamentosexames.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_medicamento = clock - paciente.tempo_entrou_fila_medicamento
            # @@@ Sorteia duração dos exames/medicamentos
            duracao_medicamentoexames = duracao_evento(EXA)
            # @@@ Agenda event_notice fim_medicamentosexames
            insere_fel((clock + duracao_medicamentoexames, 'fim_medicamentosexames', paciente, evento_fel[3]))
    # @@@ Existe paciente aguardando triagem e medicamento - NÃO
    else:
        # @@@ Existe paciente aguardando exames/medicamento?
        # @@@ Existe paciente aguardando exames/medicamento - SIM
        if len(fila_medicamentosexames) > 0:
            paciente = fila_medicamentosexames.pop(0)
            # Calcula tempo em que paciente ficou na fila
            paciente.tempo_fila_medicamento = clock - paciente.tempo_entrou_fila_medicamento
            # @@@ Sorteia duração dos exames/medicamentos
            duracao_medicamentoexames = duracao_evento(EXA)
            # @@@ Agenda event_notice fim_medicamentosexames
            insere_fel((clock + duracao_medicamentoexames, 'fim_medicamentosexames', paciente, evento_fel[3]))
        # @@@ Existe paciente aguardando exames/medicamento - NÃO
        else:
            # @@@ Existe paciente aguardando triagem?
            # @@@ Existe paciente aguardando triagem - SIM
            if (len(fila_triagem) > 0):
                paciente = fila_triagem.pop(0)
                # Calcula tempo em que paciente ficou na fila
                paciente.tempo_fila_triagem = clock - paciente.tempo_entrou_fila_triagem
                # @@@ Sorteia duração da triagem
                duracao_triagem = duracao_evento(TRI)
                # @@@ Agenda event_notice fim_triagem
                insere_fel( (clock + duracao_triagem, 'fim_triagem', paciente, evento_fel[3]) )
            # @@@ Existe paciente aguardando triagem - NÃO
            else:
                # @@@ Libera enfermerio
                evento_fel[3].libera(clock)

#####################################################################################################################
#                                                                                                                   #
#                                                        OUTROS                                                     #
#                                                                                                                   #
#####################################################################################################################

def insere_fila_cadastro(fila, paciente):
    #a fila de cadastro funciona de forma diferente das outras filas de prioridade
    inseriu = False
    if paciente.prioridade == 5:
        for i in range(len(fila)):
            if paciente.prioridade > fila[i].prioridade:
                fila.insert(i,paciente)
                inseriu = True
                break
        if not inseriu:
            fila.append(paciente)
    else:
        fila.append(paciente)

    return fila


def insere_fila_prioridade(fila, paciente):
    inseriu = False
    for i in range(len(fila)):
        if paciente.prioridade > fila[i].prioridade:
            fila.insert(i, paciente)
            inseriu = True
            break
    if not inseriu:
        fila.append(paciente)
    return fila

#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

#####################################################
#                                                   #
#                   COLEÇÕES                        #
#                                                   #
#####################################################

try:
    entrada = sys.argv[1]
    saida = sys.argv[2]
except:
    print("ERRO - PARAMETROS")
    print("python3 -B run.py entrada.txt saida.csv")
    exit()
    exit()

fel = [] # Lista temporal de atividades
clock = 0 # Clock do tempo atual
clock_anterior = 0 # Guarda o ultimo tempo antes da mudança do Clock
executa_fel = {'fim_chegada': fim_chegada, 'fim_cadastro': fim_cadastro, 'fim_triagem': fim_triagem, 'fim_atendimento': fim_atendimento, 'fim_medicamentosexames': fim_medicamentosexames}

atendentes = []
enfermeiros = []
medicos = []
pacientes = []
fila_cadastro = [] #fila de prioridade
fila_triagem = [] #fila de prioridade
fila_atendimento = [] #fila de prioridade
fila_medicamentosexames = [] #fila de prioridade

# KPI Tamanho Medio da fila
tamanho_medio_cadastro = 0
tamanho_medio_triagem = 0
tamanho_medio_atendimento = 0
tamanho_medio_medicamento = 0

prioridade_triagem = 70 # probabilidade da prioridade ser triagem

#VARIAVEIS GLOBAIS
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

#####################################################
#                                                   #
#                    EXECUÇÃO                       #
#                                                   #
#####################################################

le_arquivo(entrada)
inicializa_fel()

for i in range(ATD):
    atendentes.append(Atendente(i))
for i in range(ENF):
    enfermeiros.append(Enfermeiro(i))
for i in range(MED):
    medicos.append(Medico(i))

# Enquanto tiver eventos na FEL, a simulação continua
while (len(fel) > 0) and (clock <= TTS):

    # Essa parte é utilizada pra medir o KPI "Tamanho Medio de Fila"
    if (int(clock) > int(clock_anterior)):
        for i in range(int(clock_anterior), int(clock)):
            tamanho_medio_cadastro += len(fila_cadastro)
            tamanho_medio_triagem += len(fila_triagem)
            tamanho_medio_atendimento += len(fila_atendimento)
            tamanho_medio_medicamento += len(fila_medicamentosexames)
        clock_anterior = clock

    # Retira o evento que será computado
    evento_fel = retira_fel()
    if (evento_fel[0] > TTS):
        break
    
    # Print da FEL

    if evento_fel[0] > 60:
        horaPrint = int(evento_fel[0]/60)
        minutos = int(evento_fel[0] % 60)

    else:
        horaPrint = 0
        minutos = int(evento_fel[0])

    segundos = (evento_fel[0] - int(evento_fel[0]))*100
    if segundos > 60:
        segundos = int(segundos/60)
    else:
        segundos = int(segundos)

    if horaPrint < 10:
        hora = '0' + str(horaPrint)
    else:
        hora = str(horaPrint)

    if minutos < 10:
        hora = hora + 'h: 0' + str(minutos)
    else:
        hora = hora +'h:'+str(minutos)

    if segundos <10:
        hora = hora +'min:0' + str(segundos) + 's'

    else:
        hora = hora +'min:'+str(segundos) + 's'
    """
    if evento_fel[3] != None:
        print('Retirou da FEL: ' + str(evento_fel[1]) + '| hora: ' + hora + ' | paciente: '+str(evento_fel[2].id+1)+' | '+ str(evento_fel[3].cargo) +': '+ str(evento_fel[3].id+1))
    else:
        print('Retirou da FEL: ' + str(evento_fel[1]) + '| hora: ' +hora+ ' | paciente: '+ str(evento_fel[2].id+1))
    """

    # Muda o relogio para o tempo atual
    clock = evento_fel[0]

    # O nome função no qual se deve executar esta contida em evento_fel[1], e o executa_fel redireciona para a função correta.
    executa_fel[evento_fel[1]](evento_fel)

# Garantia de que o clock atualizou para o ultimo horario valido da execução
clock = TTS

# KPIs

# OCIOSIDADE
# Tempo ocioso dos Atendentes
total_atendentes = 0 
for atendente in atendentes:
    # Se estava ocioso na hora da finalização, calcula seu tempo ocioso
    if atendente.ocupado == False:
        atendente.set_tempo_ocioso(clock)
    total_atendentes += atendente.total_ocioso
# Tempo ocioso dos Enfermeiros
total_enfermeiros = 0
for enfermeiro in enfermeiros:
    if enfermeiro.ocupado == False:
        enfermeiro.set_tempo_ocioso(clock)
    total_enfermeiros += enfermeiro.total_ocioso
# Tempo ocioso dos Medicos
total_medicos = 0
for medico in medicos:
    if (medico.ocupado == False):
        medico.set_tempo_ocioso(clock)
    total_medicos += medico.total_ocioso
oa = total_atendentes / (TTS * len(atendentes))
oe = total_enfermeiros / (TTS * len(enfermeiros))
om = total_medicos / (TTS * len(medicos))
# Tempo ocioso geral
og = (oa + oe + om) / 3

# TEMPO MEDIO DE FILA
# Se ainda existe pacientes em alguma fila, conta quanto tempo ele ficou
for paciente in fila_cadastro:
    paciente.tempo_fila_cadastro = clock - paciente.tempo_entrou_fila_cadastro
for paciente in fila_triagem:
    paciente.tempo_fila_triagem = clock - paciente.tempo_entrou_fila_triagem
for paciente in fila_atendimento:
    paciente.tempo_fila_atendimento = clock - paciente.tempo_entrou_fila_atendimento
for paciente in fila_medicamentosexames:
    paciente.tempo_fila_medicamento = clock - paciente.tempo_entrou_fila_medicamento
media_cadastro = 0
media_triagem = 0
media_atendimento = 0
media_medicamento = 0
paciente_medicamento = 0
prioridade1 = 0
prioridade2 = 0
prioridade3 = 0
prioridade4 = 0
prioridade5 = 0
n_prioridade1 = 0
n_prioridade2 = 0
n_prioridade3 = 0
n_prioridade4 = 0
n_prioridade5 = 0
for paciente in pacientes:
    prioridade_temp = 0
    media_cadastro += paciente.tempo_fila_cadastro
    media_triagem += paciente.tempo_fila_triagem
    media_atendimento += paciente.tempo_fila_atendimento
    media_medicamento += paciente.tempo_fila_medicamento
    if (paciente.exame_medi):
        paciente_medicamento += 1
    if (paciente.prioridade == 1):
        prioridade_temp += paciente.tempo_fila_cadastro
        prioridade_temp += paciente.tempo_fila_triagem
        prioridade_temp += paciente.tempo_fila_atendimento
        prioridade_temp += paciente.tempo_fila_medicamento
        prioridade1 += prioridade_temp / 4
        n_prioridade1 += 1
    elif (paciente.prioridade == 2):
        prioridade_temp += paciente.tempo_fila_cadastro
        prioridade_temp += paciente.tempo_fila_triagem
        prioridade_temp += paciente.tempo_fila_atendimento
        prioridade_temp += paciente.tempo_fila_medicamento
        prioridade2 += prioridade_temp / 4
        n_prioridade2 += 1
    elif (paciente.prioridade == 3):
        prioridade_temp += paciente.tempo_fila_cadastro
        prioridade_temp += paciente.tempo_fila_triagem
        prioridade_temp += paciente.tempo_fila_atendimento
        prioridade_temp += paciente.tempo_fila_medicamento
        prioridade3 += prioridade_temp / 4
        n_prioridade3 += 1
    elif (paciente.prioridade == 4):
        prioridade_temp += paciente.tempo_fila_cadastro
        prioridade_temp += paciente.tempo_fila_triagem
        prioridade_temp += paciente.tempo_fila_atendimento
        prioridade_temp += paciente.tempo_fila_medicamento
        prioridade4 += prioridade_temp / 4
        n_prioridade4 += 1
    elif (paciente.prioridade == 5):
        prioridade_temp += paciente.tempo_fila_cadastro
        prioridade_temp += paciente.tempo_fila_triagem
        prioridade_temp += paciente.tempo_fila_atendimento
        prioridade_temp += paciente.tempo_fila_medicamento
        prioridade5 += prioridade_temp / 4
        n_prioridade5 += 1

media_cadastro = media_cadastro / len(pacientes)
media_triagem = media_triagem / len(pacientes)
media_atendimento = media_atendimento / len(pacientes)
try:
    media_medicamento = media_medicamento / paciente_medicamento
except:
    media_medicamento = 0
if (n_prioridade1 == 0):
    n_prioridade1 = 1
if (n_prioridade2 == 0):
    n_prioridade2 = 1
if (n_prioridade3 == 0):
    n_prioridade3 = 1
if (n_prioridade4 == 0):
    n_prioridade4 = 1
if (n_prioridade5 == 0):
    n_prioridade5 = 1
tep1 = prioridade1 / n_prioridade1
tep2 = prioridade2 / n_prioridade2
tep3 = prioridade3 / n_prioridade3
tep4 = prioridade4 / n_prioridade4
tep5 = prioridade5 / n_prioridade5
tec = media_cadastro
tet = media_triagem
tea = media_atendimento
tem = media_medicamento
# Tempo medio de fila geral
teg = (tec + tet + tea + tem) / 4 

# TAMANHO MEDIO DE FILA
tac = tamanho_medio_cadastro / TTS
tat = tamanho_medio_triagem / TTS
taa = tamanho_medio_atendimento / TTS
tam = tamanho_medio_medicamento / TTS
# Tamanho medio de fila geral
tag = (tac + tat + taa + tam) / 4

with open(saida, 'a+') as file:
    file.write(
        str("%.2f"%og)+'\t'+
        str("%.2f"%oa)+'\t'+
        str("%.2f"%oe)+'\t'+
        str("%.2f"%om)+'\t'+
        str("%.2f"%teg)+'\t'+
        str("%.2f"%tep1)+'\t'+
        str("%.2f"%tep2)+'\t'+
        str("%.2f"%tep3)+'\t'+
        str("%.2f"%tep4)+'\t'+
        str("%.2f"%tep5)+'\t'+
        str("%.2f"%tec)+'\t'+
        str("%.2f"%tet)+'\t'+
        str("%.2f"%tea)+'\t'+
        str("%.2f"%tem)+'\t'+
        str("%.2f"%tag)+'\t'+
        str("%.2f"%tac)+'\t'+
        str("%.2f"%tat)+'\t'+
        str("%.2f"%taa)+'\t'+
        str("%.2f"%tam)+'\n')