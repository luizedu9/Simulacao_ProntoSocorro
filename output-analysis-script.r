#
# Script para analise de dados de resultados da simulacao
#

library('R.utils')

# Calcula o intervalo de confianca para um unico indicador de
# desempenho de saida da simulacao
IntervaloConfianca <- function(nome, amostra, num.observacoes, alpha)
{
	# Calculando a media e desvio amostral
	Media  <- mean(amostra);
	Desvio <- sd(amostra);

	# Calculando a probabilidade (1-alpha)%
	Prob   <- 1 - alpha/2;

	# Calculando a amplitude do intervalo
	H      <- qt(p=Prob, df=(num.observacoes - 1)) * Desvio / sqrt(num.observacoes);

	# Imprimindo o resultados:
	cat(nome, ': média = ', Media, ', desvio = ', Desvio, ', [ ', Media - H, ';', Media + H, ']\n');
}

#
# Calcula intervalo de confianca para diferenca de duas amostras com mesmo
# numero de observacoes
#
IntervaloConfianca2AmostasNIguais <- function(nome, amostra1, amostra2, num.obs, alpha)
{
	# Calcula a amostra com as diferencas
	Diferenca <- amostra1 - amostra2;
	cat('Media : ', mean(Diferenca), '\n');
	cat('Desvio: ', sd(Diferenca), '\n');

	# Media e desvio
	Media  <- mean(Diferenca);
	Desvio <- sd(Diferenca);

	# Calculando a probabilidade (1-alpha)%
	Prob   <- (1 - alpha/2);

	# Calculando a amplitude do intervalo
	cat('Estat. t : ', qt(p=Prob, df=(num.obs - 1)), '\n');

	H      <- qt(p=Prob, df=(num.obs - 1)) * Desvio / sqrt(num.obs);

	cat('H = ', H, '\n');

	# Calcula limites do intervalo
	Inferior <- Media - H;
	Superior <- Media + H;

	cat(nome, ': [', Inferior, ';', Superior, ']\n');

	# Classifica de acordo com os limites do intervalo
	Classificacao <- NA;
	if(Inferior < 0 && Superior > 0)
	{
		Classificacao <- 0;
	}
	else
	{
		if(Inferior < 0 && Superior < 0)
		{
			Classificacao <- -1;
		}
		else
		{
			Classificacao <- +1;
		}
	}

	# Retorna a classificacao
	return(Classificacao)
}

#
# Calcula o I.C. para duas amostras de tamanhos diferentes
#
IntervaloConfianca2AmostasNDiferentes <- function(nome, amostra1, amostra2, num.obs, alpha)
{
	# Obtem as dimensoes de cada amostra
	n1 <- length(amostra1);
	n2 <- length(amostra2);

	# Calcula as medias e desvios
	media1      <- mean(amostra1);
	media2      <- mean(amostra2);
	desvio1     <- sd(amostra1);
	desvio2     <- sd(amostra2);

	# Calcula o grau de liberdade para calculo da estatistica t
	numerador   <- (desvio1^2/n1 + desvio2^2/n2)^2;
	denominador <- ((desvio1^2/n1)^2)/(n1-1)  + ((desvio2^2/n2)^2)/(n2-1);
	grau        <- ceiling(numerador / denominador);

	# Calcula a amplitude do intervalo de confianca
	Prob	     <- (1 - alpha/2);
	H            <- qt(p=Prob, df=grau) * sqrt(desvio1^2/n1 + desvio2^2/n2);

	# Calcula os limites do intervalo de confianca
	Inferior     <- (media1 - media2) - H;
	Superior     <- (media1 - media2) + H;

	# Classifica o intervalo
	Classificacao <- NA;
	if(Inferior < 0 && Superior > 0)
	{
		Classificacao <- 0;
	}
	else
	{
		if(Inferior < 0 && Superior < 0)
		{
			Classificacao <- -1;
		}
		else
		{
			Classificacao <- +1;
		}
	}

	# Retorna a classificacao
	return(Classificacao)
}

#
# Faz analise sobre o desempenho de duas amostras
#
Analisa2Amostras <- function(nome, amostra1, amostra2)
{
	# Calcula as estatisticas das amostras informadas
	Media1   <- mean(amostra1);
	Media2   <- mean(amostra2);
	Desvio1  <- sd(amostra1);
	Desvio2  <- sd(amostra2);
	Min1     <- min(amostra1);
	Min2     <- min(amostra2);
	Max1     <- max(amostra1);
	Max2     <- max(amostra2);
	Mediana1 <- quantile(amostra1, 0.5);
	Mediana2 <- quantile(amostra1, 0.5);

	cat('Analisando Variável ', nome, '\n\n');
	printf('%16s %16s %16s\n', 'Medida', 'Amostra1', 'Amostra2');
	printf('%16s %16f %16f\n', 'Minimo', Min1, Min2);
	printf('%16s %16f %16f\n', 'Media', Media1, Media2);
	printf('%16s %16f %16f\n', 'Mediana', Mediana1, Mediana2);
	printf('%16s %16f %16f\n', 'Desvio', Desvio1, Desvio2);
	printf('%16s %16f %16f\n', 'Maximo', Max1, Max2);

	# Calcula o numero de observacoes de ambas
	n1 <- length(amostra1);
	n2 <- length(amostra2);

	# Chama funcao de acordo com o tamanho das amostras
	if(n1 == n2)
	{
		Resultado <- IntervaloConfianca2AmostasNIguais(nome, amostra1, amostra2, n1, 0.05)
	}
	else
	{
		Resultado <- IntervaloConfianca2AmostasNDiferentes(nome, amostra1, amostra2, n1, 0.05)
	}

	# Imprime resultado textualmente
	if(Resultado == 0)
	{
		cat('Nao é possivel diferenciar amostra1 e amostra2\n');
	}
	if(Resultado == -1)
	{
		cat('A amostra1 tem media < amostra2\n');
	}
	if(Resultado == +1)
	{
		cat('A amostra1 tem media > amostra2\n');
	}
}

amostra1 <- read.csv(file="amostra1.csv", header=TRUE, sep="\t")
amostra2 <- read.csv(file="amostra2.csv", header=TRUE, sep="\t")

cat('\nMEAN IDLE TIME\n\n')
Analisa2Amostras("MEAN IDLE TIME", amostra1[,1], amostra2[,1])

cat('\nmean_idle_time-Attendant\n\n')
Analisa2Amostras("mean_idle_time-Attendant", amostra1[,2], amostra2[,2])

cat('\nmean_idle_time-Nurse\n\n')
Analisa2Amostras("mean_idle_time-Nurse", amostra1[,3], amostra2[,3])

cat('\nmean_idle_time-Doctor\n\n')
Analisa2Amostras("mean_idle_time-Doctor", amostra1[,4], amostra2[,4])

cat('\nmean_waiting_time\n\n')
Analisa2Amostras("mean_waiting_time", amostra1[,5], amostra2[,5])

cat('\nmean_waiting_time-1\n\n')
Analisa2Amostras("mean_waiting_time-1", amostra1[,6], amostra2[,6])

cat('\nmean_waiting_time-2\n\n')
Analisa2Amostras("mean_waiting_time-2", amostra1[,7], amostra2[,7])

cat('\nmean_waiting_time-3\n\n')
Analisa2Amostras("mean_waiting_time-3", amostra1[,8], amostra2[,8])

cat('\nmean_waiting_time-4\n\n')
Analisa2Amostras("mean_waiting_time-4", amostra1[,9], amostra2[,9])

cat('\nmean_waiting_time-5\n\n')
Analisa2Amostras("mean_waiting_time-5", amostra1[,10], amostra2[,10])

cat('\nmean_waiting_time-register_queue\n\n')
Analisa2Amostras("mean_waiting_time-register_queue", amostra1[,11], amostra2[,11])

cat('\nmean_waiting_time-screening_queue\n\n')
Analisa2Amostras("mean_waiting_time-screening_queue", amostra1[,12], amostra2[,12])

cat('\nmean_waiting_time-consultation_queue\n\n')
Analisa2Amostras("mean_waiting_time-consultation_queue", amostra1[,13], amostra2[,13])

cat('\nmean_waiting_time-exams_queue\n\n')
Analisa2Amostras("mean_waiting_time-exams_queue", amostra1[,14], amostra2[,14])

cat('\nmean_queue_len\n\n')
Analisa2Amostras("mean_queue_len", amostra1[,15], amostra2[,15])

cat('\nmean_queue_len-register_queue\n\n')
Analisa2Amostras("mean_queue_len-register_queue", amostra1[,16], amostra2[,16])

cat('\nmean_queue_len-screening_queue\n\n')
Analisa2Amostras("mean_queue_len-screening_queue", amostra1[,17], amostra2[,17])

cat('\nmean_queue_len-consultation_queue\n\n')
Analisa2Amostras("mean_queue_len-consultation_queue", amostra1[,18], amostra2[,18])

cat('\nmean_queue_len-exams_queue\n\n')
Analisa2Amostras("mean_queue_len-exams_queue", amostra1[,19], amostra2[,19])
