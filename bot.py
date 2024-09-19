from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TELEGRAM_TOKEN = '8069192319:AAFSZ5KEXI-PufwhEwlCaL0KCYULp75hIbs'
API_TOKEN = '4dcb6f58e9784845588bb53b17131846'
API_URL = f'https://www.myarena.ru/api.php?query=status&token={API_TOKEN}'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your server management bot.')

async def server_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(API_URL)
    data = response.json()

    if data.get("status") == "OK":
        server_info = data.get('data', {}).get('s', {})
        players_info = data.get('data', {}).get('p', [])

        # Constructing player list
        player_list = "\n".join(
            [f"{player['name']} (Score: {player['score']}, Time: {player['time']})" for player in players_info]
        ) if players_info else "No players online"

        status_message = (
            f"Server Status: {'Online' if data.get('online') == 1 else 'Offline or Starting'}\n"
            f"Server Name: {server_info.get('name', 'N/A')}\n"
            f"Max Slots: {server_info.get('playersmax', 'N/A')}\n\n"
            f"Current Players:\n{player_list}"
        )
    else:
        status_message = f"Failed to retrieve server status. API Response: {data}"

    await update.message.reply_text(status_message)

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(API_URL)
    data = response.json()

    if data.get("status") == "OK":
        players_info = data.get('data', {}).get('p', [])

        # Constructing player list
        player_list = "\n".join(
            [f"{player['name']} (Score: {player['score']}, Time: {player['time']})" for player in players_info]
        ) if players_info else "No players online"

        players_message = (
            f"Current Players:\n{player_list}"
        )
    else:
        players_message = f"Failed to retrieve player list. API Response: {data}"

    await update.message.reply_text(players_message)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", server_status))
    application.add_handler(CommandHandler("players", list_players))

    application.run_polling()

if __name__ == '__main__':
    main()
