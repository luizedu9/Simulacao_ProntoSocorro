
'''============DECLARACAO VARIAVEIS================'''

TTS = 0 #tempo maximo de simulacao em minutos
PRO = 0 #probabilidade de necessidade de exames/medicamentos
PRI = (0,0,0,0,0) #probabilidade da prioridade de atendimento dos pacientes
MED = 0 #quatidade de medicos
ENF = 0 #quantidade de enfermeiros
ATD = 0 #quantidade de atendentes
CHE =('',0.0,0.0,0.0) #distribuicao chegada_paciente
CAD =('',0.0,0.0,0.0) #distribuicao cadastro_paciente
TRI =('',0.0,0.0,0.0) #distribuicao triagem
ATE =('',0.0,0.0,0.0) #distribuicao atendimento
EXA =('',0.0,0.0,0.0) #distribuicao exames/medicamentos
prioridade_enfermeiro_triagem = 80 #probabilidade da prioridade ser triagem
prioridade_enfermeiro_medicamentos = 20 #probabilidade da prioridade ser medicamento


'''================================================='''


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
    #print(TTS,' ',PRO, ' ',PRI,' ',MED,' ',ENF, ' ',ATD,' ',CHE,' ', CAD,' ',TRI,' ',ATE,' ',EXA)
    pass
    
# Essa função encerra todas as atividades, liberando as pessoas de sua atual tarefa
def encerra():
    pass

# Apos encerrar as atividades, novas tarefas serão iniciadas
def inicia():
    pass

inicializar()
