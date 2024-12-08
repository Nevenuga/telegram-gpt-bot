import os
import asyncio
from telethon import TelegramClient, events
import openai
from dotenv import load_dotenv

load_dotenv()

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

async def main():
    print("Запуск бота...")
    print("Процесс авторизации в Telegram")
    
    try:
        client_telegram = TelegramClient('session_name', API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
        print("Подключаемся к Telegram...")
        
        try:
            await asyncio.wait_for(client_telegram.connect(), timeout=30)
        except asyncio.TimeoutError:
            print("Превышено время ожидания подключения!")
            return
        
        print("Подключение установлено")
        
        if not await client_telegram.is_user_authorized():
            print("Требуется авторизация")
            phone = input("Введите ваш номер телефона (например, +79001234567): ")
            print(f"Отправляем код на номер {phone}")
            
            try:
                await client_telegram.send_code_request(phone)
                print("Код отправлен в Telegram")
                code = input("Введите код, который пришел в Telegram: ")
                print("Выполняем вход...")
                await client_telegram.sign_in(phone, code)
                print("Вход выполнен успешно")
            except Exception as e:
                print(f"Ошибка при авторизации: {str(e)}")
                return
        else:
            print("Уже авторизованы")
        
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
        
        await client_telegram.run_until_disconnected()
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
