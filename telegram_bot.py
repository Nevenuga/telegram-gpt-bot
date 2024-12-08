import os
import asyncio
from telethon import TelegramClient, events
import openai
from dotenv import load_dotenv
import argparse
import sys

parser = argparse.ArgumentParser(description='Telegram GPT Bot')
parser.add_argument('--env', type=str, help='Путь к .env файлу', default='.env')
parser.add_argument('--session', type=str, help='Путь к файлу сессии', default='session_name.session')
args = parser.parse_args()

load_dotenv(args.env)

SESSION_FILE = args.session

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))

openai.api_key = os.getenv('OPENAI_API_KEY')

SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT')
POSITIVE_RESPONSE = os.getenv('POSITIVE_RESPONSE')

async def check_target_message(message_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message_text}
            ],
            max_tokens=10
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error in ChatGPT API call: {e}")
        return "false"

async def authenticate_client():
    """Authenticate Telegram client, creating session if needed."""
    try:
        if os.path.exists(SESSION_FILE) and os.path.getsize(SESSION_FILE) == 0:
            print(f"Файл сессии {SESSION_FILE} пуст. Требуется новая авторизация.")
            os.remove(SESSION_FILE)

        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        
        await client.connect()
        
        if not await client.is_user_authorized():
            print("Требуется авторизация в Telegram.")
            print(f"Введите номер телефона (с кодом страны, например +79XXXXXXXXXX):")
            phone_number = input().strip()
            
            await client.send_code_request(phone_number)
            
            print("Введите код подтверждения, отправленный в Telegram:")
            code = input().strip()
            await client.sign_in(phone=phone_number, code=code)
        
        return client

    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        sys.exit(1)

async def main():
    print("Запуск бота...")
    print("Процесс авторизации в Telegram")
    
    try:
        client_telegram = await authenticate_client()
        print("Подключение установлено")
        
        @client_telegram.on(events.NewMessage)
        async def handle_new_message(event):
            print(f"\nПолучено новое сообщение в чате {event.chat_id}")
            
            if event.chat_id != TARGET_CHAT_ID:
                print(f"Это сообщение не из целевого чата (нужен {TARGET_CHAT_ID})")
                return

            message_text = event.message.text
            print(f"Получено сообщение: {message_text}")

            response = await check_target_message(message_text)
            print(f"Ответ ChatGPT: {response}")

            if response.lower() == 'true':
                print("Обнаружено Целевое сообщение")
                await event.respond(POSITIVE_RESPONSE)
            else:
                print("Это не целевое сообщение")
        
        me = await client_telegram.get_me()
        print(f"\nУспешно авторизовались как: {me.first_name} (@{me.username})")
        print(f"Бот активен и слушает сообщения в чате с ID: {TARGET_CHAT_ID}")
        print("Для остановки бота нажмите Ctrl+C")
        
        # Держим бота активным
        await client_telegram.run_until_disconnected()

    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    asyncio.run(main())
