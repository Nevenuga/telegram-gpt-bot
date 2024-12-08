# Telegram Volleyball Invitation Bot

## Описание
Телеграм-бот, который использует AI для обнаружения приглашений на волейбол в групповых чатах.

## Возможности
- Анализ сообщений в Telegram-чате
- Определение приглашений на волейбол с помощью OpenAI
- Автоматический ответ на приглашения

## Установка

### Prerequisites
- Python 3.8+
- Telegram API credentials
- OpenAI API ключ

### Шаги установки
1. Клонируйте репозиторий
```bash
git clone https://github.com/yourusername/telegram-volleyball-bot.git
cd telegram-volleyball-bot
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


