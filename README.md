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
    pip install TempoSinc
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
### Obter a media de temperatura para os proxímos sete dias  
```python
  aa = a.calcular_media_por_dia()
  print(aa)
```
Vai retornar a media de todas as unidades citadas acima.  
### Obter previsão da temperatura atual   
```python
    aa = a.obter_dados_cli_atual()
    print(aa)
```
Vai retornar os dados climáticos atuias de uma cidade.  
### Obter previsão da temperatura por hora para os proxímos sete dias  
```python
    aa = a.obter_previsao_hora_prox_7_dias()
    print(aa)
```
Vai retornar dados climaticos da semana por hora.  
### Obter previsão da temperatura por hora de um dia em específico  
```python
    aa = a.obter_dados_do_dia_atual_por_hora("2024-01-28")
    print(aa)
```
Vai retornar os dados climáticos por hora de um dia em específico.  
O parâmetro da função é a data em específico começando pelo ano, mês e dia. Utilizando aspas simples ou duplas.  
### Elaboração de um gráfico que representa a probabilidade de ocorrência de chuva nos próximos sete dias  
```python
    aa = a.visualizar_grafico_de_media_precipitacao()
```
Vai retornar um gráfico com as medias de chances de chuva para os sete dias.  
### Elaboração de um gráfico que representa a probabilidade de ocorrência de chuva por hora de um dia em específico  
```python
    aa = a.obter_dados_do_dia_atual_por_hora("2024-01-28")
    bb = a.visualizar_grafico_de_hora_precipitacao(aa)
```
Vai retornar um gráfico com as medias de chances de chuva por hora de um dia em específico.  
O parâmetro da função são os dados da função obter_dados_do_dia_atual_por_hora("2024-01-28").  
### Envio de dados climáticos por e-mail  
```python
    aa = a.obter_previsao_hora_prox_7_dias()
    bb = a.enviar_email("seu e-mail", aa)
```
Envia os dados para um e-mail em específico.  
O primeiro parâmetro é o e-mail que deseja enviar e o segundo parâmetro é o dado que deseja enviar.
