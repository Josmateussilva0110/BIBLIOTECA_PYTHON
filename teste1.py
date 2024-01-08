import requests
import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

def obter_coordenadas_por_cidade():
    # Converter a resposta JSON para um dicionário Python
    data = response.json()

    # Processar dados horários
    hourly_data = {
        "data": pd.to_datetime(data['hourly']['time'], format='%Y-%m-%dT%H:%M', errors='coerce'),
        "temperatura_2m": data['hourly']['temperature_2m'],
        "umidade_relativa_2m": data['hourly']['relative_humidity_2m'],
        "temperatura_aparente" : data['hourly']["apparent_temperature"],
        "prob_precipitacao": data['hourly']['precipitation_probability'],
        "velocidade_vento_10m": data['hourly']['wind_speed_10m']
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)


    # Dividir a coluna 'data' em 'data' e 'hora'
    hourly_dataframe['data'] = pd.to_datetime(hourly_dataframe['data'])
    hourly_dataframe['hora'] = hourly_dataframe['data'].dt.strftime('%H:%M')
    hourly_dataframe['data'] = hourly_dataframe['data'].dt.strftime('%Y-%m-%d')

    # Reorganizar as colunas
    hourly_dataframe = hourly_dataframe[['data', 'hora'] + [col for col in hourly_dataframe.columns if col not in ['data', 'hora']]]

    pd.set_option('display.max_rows', None)  # Mostrar todas as linhas
    # print(hourly_dataframe)

    return hourly_dataframe  # Retorna o DataFrame

    
def Dados_Atuais():
    # Converter a resposta JSON para um dicionário Python
    data = response.json()

    current_data = {
        "data": pd.to_datetime(data['current']['time'], format='%Y-%m-%dT%H:%M', errors='coerce'),
        "temperatura_2m": data['current']['temperature_2m'],
        "umidade_relativa_2m": data['current']['relative_humidity_2m'],
        "temperatura_aparente": data['current']['apparent_temperature'],
        "velocidade_vento_10m": data['current']['wind_speed_10m']
    }
    # Criação de hourly_dataframe1 como DataFrame com uma única linha
    hourly_dataframe1 = pd.DataFrame(data=current_data, index=[0])

    pd.set_option('display.max_rows', None)  # Mostrar todas as linhas
    # print(hourly_dataframe)

    print(hourly_dataframe1)
    
def Dados_Diarios():
    # Converter a resposta JSON para um dicionário Python
    data = response.json()

    daily_data = {
        "temperatura maxima_2m": data['daily']['temperature_2m_max'],
        "temperatura minina_2m": data['daily']['temperature_2m_min'],
        "indice UV": data['daily']['uv_index_max'],
        "Probabilidade maxima de Precipitação": data['daily']['precipitation_probability_max'],
        "Velocidade maxima do vento": data['daily']['wind_speed_10m_max']
    }
    # Criação de hourly_dataframe1 como DataFrame com uma única linha
    daily_dataframe1 = pd.DataFrame(data=daily_data)

    pd.set_option('display.max_rows', None)  # Mostrar todas as linhas
    print(daily_dataframe1)
        
def calcular_media_por_dia(dataframe):
    # Excluir a coluna 'hora' antes de calcular a média
    dataframe = dataframe.drop(columns=['hora'], errors='ignore')
    
    # Calcular a média por coluna separado por dia
    media_por_dia = dataframe.groupby('data').mean().reset_index()
    return media_por_dia

def obter_dados_por_dia(dataframe, data_selecionada):
    # Converter a coluna 'data' para o tipo datetime para garantir a comparação correta
    dataframe['data'] = pd.to_datetime(dataframe['data'])
    
    # Filtrar o DataFrame para a data selecionada
    dados_do_dia = dataframe[dataframe['data'] == pd.to_datetime(data_selecionada)].reset_index(drop=True)

    return dados_do_dia


def visualizar_grafico_de_media_precipitacao(media_por_dia):
    # Verificar se a coluna 'prob_precipitacao' existe no DataFrame
    if 'prob_precipitacao' in media_por_dia.columns:
        # Criar um gráfico de barras da média de precipitação por dia
        plt.figure(figsize=(12, 6))
        bars = plt.bar(media_por_dia['data'], media_por_dia['prob_precipitacao'], color='skyblue', alpha=0.7)
        plt.title('Média de Precipitação por Dia')
        plt.xlabel('Data')
        plt.ylabel('Média de Precipitação (%)')

        # Adicionar linhas de grade
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotacionar os rótulos do eixo x para melhor legibilidade
        plt.xticks(rotation=45, ha='right')

        # Adicionar os valores da média correspondentes acima das barras
        for i, bar in enumerate(bars):
            yval = media_por_dia['prob_precipitacao'].iloc[i]
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom', color='black')

        plt.tight_layout()  # Ajustar o layout para evitar cortes
        plt.show()
    else:
        print("Coluna 'prob_precipitacao' não encontrada no DataFrame.")
        
def visualizar_grafico_de_Hora_precipitacao(dataframe):
    # Verificar se a coluna 'prob_precipitacao' existe no DataFrame
    if 'prob_precipitacao' in dataframe.columns:
        # Criar um gráfico de barras da probabilidade de precipitação por hora
        plt.figure(figsize=(12, 6))
        bars = plt.bar(dataframe['hora'], dataframe['prob_precipitacao'], color='lightgreen', alpha=0.7)
        plt.title(f'Probabilidade de Precipitação por Hora --- Data: {dataframe["data"].iloc[0].date()}')
        plt.xlabel('Hora')
        plt.ylabel('Probabilidade de Precipitação (%)')
        
        # Adicionar linhas de grade
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.xticks(rotation=45, ha='right')

        # Adicionar os valores correspondentes acima das barras
        for i, bar in enumerate(bars):
            yval = dataframe['prob_precipitacao'].iloc[i]
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom', color='black')

        plt.tight_layout()  # Ajustar o layout para evitar cortes
        plt.show()
    else:
        print("Coluna 'prob_precipitacao' não encontrada no DataFrame.")


if __name__ == "__main__":
    # Solicitar ao usuário digitar o nome da cidade
    cidade_nome = "Santana do Piaui"
    
    # Instanciar o geolocalizador
    geolocator = Nominatim(user_agent="my_geocoder")

    # Pesquisar a cidade
    location = geolocator.geocode(cidade_nome)

    # Verificar se a localização foi encontrada
    if location:
        # Obter as coordenadas (latitude e longitude)
        latitude = location.latitude
        longitude = location.longitude
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
            print("Cidade não encontrada.")
    # Configurar os parâmetros da solicitação
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "wind_speed_10m"],
        "hourly": ["temperature_2m", "relative_humidity_2m","apparent_temperature", "precipitation_probability", "wind_speed_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_probability_max", "wind_speed_10m_max"],
        "timezone": "auto"
    }

    # Fazer a solicitação
    response = requests.get(url, params=params)

    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
            dataframe = obter_coordenadas_por_cidade()
            media_por_dia = calcular_media_por_dia(dataframe)
            
            # Loop principal
            while True:
                print("\nMenu:")
                print("0 - Sair")
                print("1 - Obter dados meteorológicos por Hora na cidade em 7 dias")
                print("2 - Obter dados do dia atual da Cidade")
                print("3 - Obter dados dos 7 proximos dias")
                print("4 - Obter media dos dados meteorológicos por hora dos 7 dias na cidade")
                print("5 - Obter dados da Hora por data na cidade")
                print("6 - Visualizar por gráfico a media de chance de precipitação nos proximos 7 dias na Cidade")
                print("7 - Visualizar por gráfico (Hora) a chance de precipitação na Cidade")
                
                opcao = input("Escolha uma opção: ")
                
                if opcao == "0":
                    break
                elif opcao == "1":
                    # dataframe = obter_coordenadas_por_cidade(latitude, longitude)
                    print(dataframe)
                elif opcao == "2":
                    Dados_Atuais()
                elif opcao == "3":
                    Dados_Diarios()
                elif opcao == "4": 
                        # media_por_dia = calcular_media_por_dia(dataframe)
                        print(media_por_dia)
                elif opcao == "5":
                    data_selecionada = input("Digite a data no formato YYYY-MM-DD: ")
                    novo_dataframe = obter_dados_por_dia(dataframe, data_selecionada)
                    
                    if novo_dataframe is not None:
                        print("\nNovo DataFrame:")
                        print(novo_dataframe)

                    else:
                        print(f"Nenhum dado disponível para a data {data_selecionada}.")
                        
                elif opcao == "6":
                    visualizar_grafico_de_media_precipitacao(media_por_dia)
                    
                elif opcao == "7":
                    try:
                        visualizar_grafico_de_Hora_precipitacao(novo_dataframe)
                    except:
                        print("Execute o item 3 primeiro.")
                else:
                    print("Opção inválida. Tente novamente.\n")
        
    else:
        print(f"A solicitação falhou com o código de status: {response.status_code}")
    
