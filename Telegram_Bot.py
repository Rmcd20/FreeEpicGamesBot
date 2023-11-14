import telebot
import requests
import time

CHAVE_API_TELEGRAM = "Seu_tokenApi_Bot"
BOT_TELEGRAM = telebot.TeleBot(CHAVE_API_TELEGRAM)

# URL da API de jogos grátis da Epic Games
API_EPIC_GAMES_URL = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions'

# Lógica para obter informações sobre jogos grátis da Epic Games
def obter_informacoes_jogos():
    try:
        # Faz uma requisição GET para a API da Epic Games
        response = requests.get(API_EPIC_GAMES_URL)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Extrai as informações relevantes da resposta
        free_games = response.json()['data']['Catalog']['searchStore']['elements']

        # Filtra apenas os jogos grátis
        free_games_info = [
            {
                'title': game['title'],
                'price': game['price']['totalPrice']['fmtPrice']['originalPrice'],
                'startDate': game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'],
                'endDate': game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'],
            }
            for game in free_games if game.get('promotions') and game['promotions']['promotionalOffers']
        ]

        return free_games_info

    except requests.exceptions.RequestException as e:
        # Trata erros durante a obtenção das informações
        raise Exception(f"Erro ao obter informações sobre jogos grátis: {e}")

@BOT_TELEGRAM.message_handler(commands=['start'])
def handle_start(message):
    BOT_TELEGRAM.send_message(message.chat.id, "Bem-vindo! Eu sou um bot que avisa sobre jogos grátis da Epic Games. Para obter informações, use o comando /jogosgratisepic.")

@BOT_TELEGRAM.message_handler(commands=['jogosgratisepic'])
def handle_jogos_gratis_epic(message):
    try:
        # Obtém as informações sobre jogos grátis diretamente da API da Epic Games
        info_jogos = obter_informacoes_jogos()

        # Formata as informações para envio
        formatted_info = "\n".join([f"{game['title']} - {game['price']} ({game['startDate']} - {game['endDate']})" for game in info_jogos])

        # Envia as informações para o chat do Telegram
        BOT_TELEGRAM.send_message(message.chat.id, f"Os jogos grátis da Epic Games são:\n{formatted_info}")

    except Exception as e:
        # Tratamento de erro, se necessário
        print(e)
        BOT_TELEGRAM.send_message(message.chat.id, "Desculpe, não foi possível obter informações sobre jogos grátis no momento.")

def iniciar_bot():
    while True:
        try:
            BOT_TELEGRAM.polling()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Reiniciando o bot em 20 segundos...")
            time.sleep(20)

if __name__ == "__main__":
    iniciar_bot()
