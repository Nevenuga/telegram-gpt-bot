# Telegram GPT Bot

## Описание
Телеграм-бот, который использует AI для обнаружения целевого сообщения и ответа на него в групповых чатах и ЛС.

## Возможности
- Анализ сообщений в Telegram-чате
- Определение целевого сообщения с помощью OpenAI
- Автоматический ответ от лица пользователя

## Установка

### Prerequisites
- Python 3.8+
- Telegram API credentials
- OpenAI API ключ

### Шаги установки
1. Клонируйте репозиторий
```bash
git clone https://github.com/Nevenuga/telegram-gpt-bot.git
cd telegram-gpt-bot
```

2. Установите зависимости
```bash
pip install -r requirements.txt
```

3. Создайте `.env` файл на основе `.env.example`
```bash
cp .env.example .env
```

4. Заполните `.env` файл вашими API ключами

## Запуск
```bash
python telegram_bot.py
```
