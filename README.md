# Simulacao_ProntoSocorro

Instituto Federal de Educação, Ciência e Tecnologia de Minas Gerais, IFMG - Campus Formiga

Ciência da Computação

Simulação de um Pronto Socorro em Python para a disciplina Introdução à Simulação.

Autores:
Bruna Cristina Mendes,
Flávia Santos Ribeiro,
Luiz Eduardo Pereira. 

# Artigo

Este trabalho foi utilizado para uma publicação de artigo no III Seminário de Pesquisa e Inovação do IFMG – Campus Formiga. 

[Artigo](https://github.com/luizedu9/Artigo)

# Objetivo:

O objetivo deste trabalho era criar um simulador para um Pronto Socorro para sugerir mudanças na composição de funcionarios.
Para isso leva-se em conta 3 KPIs (Key Performance Indicator) medidos. Ociosidade, Tempo Medio em Fila e Tamanho Medio em Fila.
Para entender como o simulador funciona, olhar o DCA (Diagrama de Ciclo de Atividades) e os Envent Listeners disponiveis na pasta Projeto.

# Execução:

python3 run.py config.txt saida.csv

run.py executa 100 simulações consecutivas armazenando os resultados em um arquivo de extensão CSV.
config.txt possui todos os parametros de entrada do programa, como tempo de simulação, número de funcionarios e distribuições de chegada de pacientes / tempo de atendimento.

Para analisar resultados entre duas amostras:

Rscript output-analysis-script.r
Arquivos necessarios: amostra1.csv, amostra2.csv

Código cedido pelo Prof. Me. Diego Mello da Silva

Referencia para as distribuições utilizadas:
Silva, L. P. “Análise de Cenários em um Sistema de Pronto Socorro
Atendimento Utilizando Simulação Discreta”. <https://bit.ly/2JelTs7>
