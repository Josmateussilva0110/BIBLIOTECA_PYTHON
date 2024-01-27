# Descrição  
A classe Temposinc foi desenvolvida como uma ferramenta versátil para a obtenção e análise de dados de previsão do tempo. Com funcionalidades abrangentes, ela permite não apenas a recuperação das coordenadas de uma cidade, mas também a obtenção detalhada da previsão do tempo para os próximos 7 dias. Além disso, oferece recursos para calcular médias diárias, visualizar probabilidades de precipitação de chuva através de gráficos interativos e até mesmo compartilhar essas informações meteorológicas por e-mail.  
# Funcionalidades  
•	Obter cordenadas de uma cidade.  
•	Obter previsão de tempo para os proxímos sete dias.  
•	Obter a media de temperatura para os proxímos sete dias.   
•	Obter previsão da temperatura atual.  
•	Obter previsão da temperatura por hora para os proxímos sete dias.  
•	Obter previsão da temperatura por hora de um dia em específico.  
•	Elaboração de um gráfico que representa a probabilidade de ocorrência de chuva nos próximos sete dias.  
•	Elaboração de um gráfico que representa a probabilidade de ocorrência de chuva por hora de um dia em específico.  
•	Envio de dados climáticos por e-mail.  
# Como usar  
### Importar a biblioteca <br>  
```python
    pip install TempoSinc==0.0.2
```

### Cria a instância da classe passando o nome da cidade como parâmetro 
```python
    a = Temposinc("picos")
```

# Usando metodos:  
### Obter cordenadas de uma cidade  
```python
    aa = a.obter_coordenadas()
    print(aa)
```
Vai retornar a latitude e longitude da cidade escolhida.  
### Obter previsão de tempo para os proxímos sete dias

```python
  aa = a.dados_diarios_prox_7_dias()
  print(aa)
```
Vai retornar dados como temperatura máxima, temperatura minima, indice UV, probabilidade de chuva e velocidade do vento.
