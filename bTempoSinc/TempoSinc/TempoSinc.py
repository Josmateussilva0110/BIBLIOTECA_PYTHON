import requests
import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Temposinc:
    """ 
    Uma classe para obter e processar dados de previsão do tempo.
    Fornece métodos para obter previsões meteorológicas por hora e diárias, calcular médias diárias,
    e visualizar dados de precipitação por meio de gráficos. Também inclui funcionalidades
    para enviar dados meteorológicos por e-mail.

    Attributes:
        cidade_nome (str): O nome da cidade para a qual a previsão do tempo é obtida.
        geolocator (Nominatim): Uma instância da classe geopy.geocoders.Nominatim para obter
                                coordenadas de latitude e longitude da cidade especificada.
        latitude (float): A coordenada de latitude da cidade.
        longitude (float): A coordenada de longitude da cidade.
        url (str): A URL base para a API Open-Meteo.
        params (dict): Parâmetros para a solicitação à API, incluindo latitude, longitude e tipos de dados meteorológicos.
        response (Response): O objeto de resposta obtido da solicitação à API.
        dataframe (DataFrame): DataFrame Pandas contendo os dados de previsão do tempo por hora.
        media_por_dia (DataFrame): DataFrame Pandas contendo a média diária dos dados meteorológicos.

    Methods:
        obter_coordenadas(): Obtém as coordenadas de latitude e longitude da cidade especificada.
        obter_previsao_hora_prox_7_dias(): Extrai e formata dados de previsão do tempo por hora para os próximos 7 dias.
        calcular_media_por_dia(): Calcula a média diária dos dados meteorológicos.
        obter_dados_cli_atual(): Obtém os dados meteorológicos atuais para a cidade especificada.
        dados_diarios_prox_7_dias(): Extrai e formata dados de previsão do tempo diários para os próximos 7 dias.
        obter_dados_do_dia_atual_por_hora(data_selecionada): Extrai dados meteorológicos por hora para uma data específica.
        visualizar_grafico_de_media_precipitacao(): Exibe um gráfico de barras mostrando a média de precipitação para os próximos 7 dias.
        visualizar_grafico_de_hora_precipitacao(dataframe): Exibe um gráfico de barras mostrando a precipitação por hora para uma data específica.
        enviar_email(destinatario, dataframe): Envia dados meteorológicos por e-mail para o destinatário especificado. """
    
    def __init__(self, cidade_nome):
        self.cidade_nome = cidade_nome
        self.geolocator = Nominatim(user_agent="my_geocoder")
        self.latitude, self.longitude = self.obter_coordenadas()

        # Configurar os parâmetros da solicitação
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "wind_speed_10m"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "wind_speed_10m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_probability_max", "wind_speed_10m_max"],
            "timezone": "auto"
        }

        # Fazer a solicitação
        self.response = requests.get(self.url, params=self.params)

        # Verificar se a solicitação foi bem-sucedida (código de status 200)
        if self.response.status_code == 200:
            self.dataframe = self.obter_previsao_hora_prox_7_dias()
            self.media_por_dia = self.calcular_media_por_dia()

            # # Loop principal
            # while True:
            #     self.exibir_menu()
        else:
            print(f"A solicitação falhou com o código de status: {self.response.status_code}")

    def obter_coordenadas(self):
        """
        Obtém as coordenadas de latitude e longitude da cidade especificada.

        Returns:
        -------
        tuple
            Uma tupla contendo as coordenadas de latitude e longitude, respectivamente.

        Se a cidade não for encontrada, imprime uma mensagem de erro e encerra o programa.
        """

        location = self.geolocator.geocode(self.cidade_nome)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            # print(f"Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
        else:
            print("Cidade não encontrada.")
            exit()

    def obter_previsao_hora_prox_7_dias(self):##
        """
        Obtém e formata os dados de previsão do tempo por hora para os próximos 7 dias.

        Returns:
        -------
        DataFrame
            Um DataFrame Pandas contendo as previsões meteorológicas por hora.

        Utiliza a resposta da solicitação à API para extrair informações como temperatura, umidade,
        temperatura aparente, probabilidade de precipitação e velocidade do vento por hora. Formata
        esses dados em um DataFrame e adiciona colunas para data, hora e organiza a ordem das colunas.
        """

        data = self.response.json()
        hourly_data = {
            "data": pd.to_datetime(data['hourly']['time'], format='%Y-%m-%dT%H:%M', errors='coerce'),
            "temperatura_2m": data['hourly']['temperature_2m'],
            "umidade_relativa_2m": data['hourly']['relative_humidity_2m'],
            "temperatura_aparente": data['hourly']["apparent_temperature"],
            "prob_precipitacao": data['hourly']['precipitation_probability'],
            "velocidade_vento_10m": data['hourly']['wind_speed_10m']
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe['data'] = pd.to_datetime(hourly_dataframe['data'])
        hourly_dataframe['hora'] = hourly_dataframe['data'].dt.strftime('%H:%M')
        hourly_dataframe['data'] = hourly_dataframe['data'].dt.strftime('%Y-%m-%d')
        hourly_dataframe = hourly_dataframe[['data', 'hora'] + [col for col in hourly_dataframe.columns if col not in ['data', 'hora']]]
        pd.set_option('display.max_rows', None)
        
        return hourly_dataframe

    def calcular_media_por_dia(self):##
        """
        Calcula a média diária dos dados meteorológicos.

        Returns:
        -------
        DataFrame
            Um DataFrame Pandas contendo a média diária dos dados meteorológicos.

        Remove a coluna 'hora' do DataFrame original, se existir, e calcula a média dos valores
        agrupados por data. O resultado é um novo DataFrame contendo a média diária dos dados.
        """

        dataframe = self.dataframe.drop(columns=['hora'], errors='ignore')
        media_por_dia = dataframe.groupby('data').mean().reset_index()
        return media_por_dia

    # def exibir_menu(self):
    #     print("\nMenu:")
    #     print("0 - Sair")
    #     print("1 - Obter dados meteorológicos por Hora na cidade em 7 dias")
    #     print("2 - Obter dados do dia atual da Cidade")
    #     print("3 - Obter dados dos 7 próximos dias")
    #     print("4 - Obter média dos dados meteorológicos por hora dos 7 dias na cidade")
    #     print("5 - Obter dados da Hora por data na cidade")
    #     print("6 - Visualizar por gráfico a média de chance de precipitação nos próximos 7 dias na Cidade")
    #     print("7 - Visualizar por gráfico (Hora) a chance de precipitação na Cidade")

    #     opcao = input("Escolha uma opção: ")

    #     if opcao == "0":
    #         exit()
    #     elif opcao == "1":
    #         print(self.dataframe)
    #         op = input("Deseja receber esses dados por email?(S/N)").upper()
    #         if op == "S":
    #             destinatario = input("Digite o endereço de e-mail do destinatário: ")
    #             self.enviar_email(destinatario, self.dataframe)
    #     elif opcao == "2":
    #         df = self.obter_dados_cli_atual()
    #         print(df)
    #         op = input("Deseja receber esses dados por email?(S/N)").upper()
    #         if op == "S":
    #             destinatario = input("Digite o endereço de e-mail do destinatário: ")
    #             self.enviar_email(destinatario, df)
    #     elif opcao == "3":
    #         df = self.dados_diarios_prox_7_dias()
    #         print(df)
    #         op = input("Deseja receber esses dados por email?(S/N)").upper()
    #         if op == "S":
    #             destinatario = input("Digite o endereço de e-mail do destinatário: ")
    #             self.enviar_email(destinatario, df)
    #     elif opcao == "4":
    #         print(self.media_por_dia)
    #     elif opcao == "5":
    #         data_selecionada = input("Digite a data no formato YYYY-MM-DD: ")
    #         novo_dataframe = self.obter_dados_do_dia_atual_por_hora(data_selecionada)
    #         if novo_dataframe is not None:
    #             print("\nNovo DataFrame:")
    #             print(novo_dataframe)
    #         else:
    #             print(f"Nenhum dado disponível para a data {data_selecionada}.")
    #         op = input("Deseja receber esses dados por email?(S/N)").upper()
    #         if op == "S":
    #             destinatario = input("Digite o endereço de e-mail do destinatário: ")
    #             self.enviar_email(destinatario, novo_dataframe)
    #     elif opcao == "6":
    #         self.visualizar_grafico_de_media_precipitacao()
    #     elif opcao == "7":
    #         data_selecionada = input("Digite a data no formato YYYY-MM-DD: ")
    #         novo_dataframe = self.obter_dados_do_dia_atual_por_hora(data_selecionada)
    #         if novo_dataframe is not None:
    #             self.visualizar_grafico_de_hora_precipitacao(novo_dataframe)
    #         else:
    #             print(f"Nenhum dado disponível para a data {data_selecionada}.")
    #     else:
    #         print("Opção inválida. Tente novamente.\n")

    def obter_dados_cli_atual(self):
        """
        Obtém os dados meteorológicos atuais para a cidade especificada.

        Returns:
        -------
        DataFrame
            Um DataFrame Pandas contendo os dados meteorológicos atuais.

        Extrai informações como temperatura, umidade, temperatura aparente e velocidade do vento
        a partir da resposta da solicitação à API. Formata esses dados em um DataFrame, criando
        uma única linha com os valores atuais.
        """

        data = self.response.json()
        current_data = {
            "data": pd.to_datetime(data['current']['time'], format='%Y-%m-%dT%H:%M', errors='coerce'),
            "temperatura_2m": data['current']['temperature_2m'],
            "umidade_relativa_2m": data['current']['relative_humidity_2m'],
            "temperatura_aparente": data['current']['apparent_temperature'],
            "velocidade_vento_10m": data['current']['wind_speed_10m']
        }
        hourly_dataframe1 = pd.DataFrame(data=current_data, index=[0])
        pd.set_option('display.max_rows', None)
        
        
        return hourly_dataframe1

    def dados_diarios_prox_7_dias(self):
        """
        Extrai e formata dados de previsão do tempo diários para os próximos 7 dias.

        Returns:
        -------
        DataFrame
            Um DataFrame Pandas contendo as previsões meteorológicas diárias.

        Utiliza a resposta da solicitação à API para extrair informações como temperatura máxima,
        temperatura mínima, índice UV, probabilidade máxima de precipitação e velocidade máxima do vento
        para cada dia. Formata esses dados em um DataFrame.
        """

        data = self.response.json()
        daily_data = {
            "temperatura_maxima_2m": data['daily']['temperature_2m_max'],
            "temperatura_minina_2m": data['daily']['temperature_2m_min'],
            "indice_UV": data['daily']['uv_index_max'],
            "Probabilidade_maxima_de_Precipitacao": data['daily']['precipitation_probability_max'],
            "Velocidade_maxima_do_vento": data['daily']['wind_speed_10m_max']
        }
        daily_dataframe1 = pd.DataFrame(data=daily_data)
        pd.set_option('display.max_rows', None)
        
        return daily_dataframe1

    def obter_dados_do_dia_atual_por_hora(self, data_selecionada):
        """
        Extrai dados meteorológicos por hora para uma data específica.

        Parameters
        ----------
            data_selecionada (str): 
                A data no formato YYYY-MM-DD para a qual os dados serão extraídos.

        Returns
        -------
            DataFrame:
                Um DataFrame Pandas contendo os dados meteorológicos por hora para a data especificada.

        Cria uma cópia do DataFrame original, converte a coluna 'data' para o tipo datetime e filtra os dados
        para incluir apenas as entradas correspondentes à data especificada. Retorna o DataFrame resultante.
        """

        dataframe = self.dataframe.copy()
        dataframe['data'] = pd.to_datetime(dataframe['data'])
        dados_do_dia = dataframe[dataframe['data'] == pd.to_datetime(data_selecionada)].reset_index(drop=True)
        
        return dados_do_dia

    def visualizar_grafico_de_media_precipitacao(self):
        """
        Exibe um gráfico de barras mostrando a média de precipitação para os próximos 7 dias.

        Verifica se a coluna 'prob_precipitacao' está presente no DataFrame de média diária.
        Se presente, gera um gráfico de barras utilizando os dados dessa coluna, exibindo a média
        de precipitação para cada dia. Caso contrário, imprime uma mensagem de erro.
        """

        if 'prob_precipitacao' in self.media_por_dia.columns:
            plt.figure(figsize=(12, 6))
            bars = plt.bar(self.media_por_dia['data'], self.media_por_dia['prob_precipitacao'], color='skyblue', alpha=0.7)
            plt.title('Média de Precipitação por Dia')
            plt.xlabel('Data')
            plt.ylabel('Média de Precipitação (%)')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45, ha='right')
            for i, bar in enumerate(bars):
                yval = self.media_por_dia['prob_precipitacao'].iloc[i]
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom', color='black')
            plt.tight_layout()
            plt.show()

        else:
            print("Coluna 'prob_precipitacao' não encontrada no DataFrame.")


    def visualizar_grafico_de_hora_precipitacao(self, dataframe):
        """
        Exibe um gráfico de barras mostrando a probabilidade de precipitação por hora para uma data específica.

        Parameters
        ----------
        dataframe (DataFrame): 
            Um DataFrame Pandas contendo os dados meteorológicos por hora para a data especificada.

        Verifica se a coluna 'prob_precipitacao' está presente no DataFrame fornecido.
        Se presente, gera um gráfico de barras utilizando os dados dessa coluna, exibindo a probabilidade
        de precipitação para cada hora. Caso contrário, imprime uma mensagem de erro.
        """

        if 'prob_precipitacao' in dataframe.columns:
            plt.figure(figsize=(12, 6))
            bars = plt.bar(dataframe['hora'], dataframe['prob_precipitacao'], color='lightgreen', alpha=0.7)
            plt.title(f'Probabilidade de Precipitação por Hora --- Data: {dataframe["data"].iloc[0]}')
            plt.xlabel('Hora')
            plt.ylabel('Probabilidade de Precipitação (%)')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45, ha='right')
            for i, bar in enumerate(bars):
                yval = dataframe['prob_precipitacao'].iloc[i]
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom', color='black')
            plt.tight_layout()
            plt.show()

        else:
            print("Coluna 'prob_precipitacao' não encontrada no DataFrame ou dados não disponíveis para a data.")

    def enviar_email(self, destinatario, dataframe):
        """
        Envia um e-mail com os dados meteorológicos para o destinatário especificado.

        Parameters
        ----------
            destinatario (str): O endereço de e-mail do destinatário.
            dataframe (DataFrame): Um DataFrame Pandas contendo os dados meteorológicos.

        Utiliza o servidor SMTP do Gmail para enviar um e-mail contendo os dados meteorológicos
        formatados como texto. O e-mail é enviado para o destinatário especificado.
        """

        servidor_email = "temposinc.gerencia@gmail.com"
        senha_email = "expo fepk nqts gjyb"
        servidor_smtp = "smtp.gmail.com"
        porta_smtp = 587

        msg = MIMEMultipart()
        msg['From'] = servidor_email
        msg['To'] = destinatario
        msg['Subject'] = 'Clima'

        corpo_email = "Dados Meteorológicos por Hora:\n\n" + dataframe.to_string()
        msg.attach(MIMEText(corpo_email))

        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(servidor_email, senha_email)
            server.sendmail(servidor_email, destinatario, msg.as_string())

        print(f"E-mail enviado para {destinatario} com sucesso!")


if __name__ == "__main__":
    cidade_nome = "Santana do Piaui"
    app = Temposinc(cidade_nome)
