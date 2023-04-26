![233348780-313ad8af-8fa5-47e0-x8cvfd1c-7f0aea8c24a122](https://user-images.githubusercontent.com/112638163/234632117-c09cbbb2-0453-4f23-b49a-480af6e9d3b5.png)

### Telegram-bot
```
Телеграм-бот для отслеживания статуса проверки домашней работы на Яндекс.Практикум.
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.
```

### Технологии:
- Python 3.9
- python-dotenv 0.19.0
- python-telegram-bot 13.7

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:0z0nize/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
- токен профиля на Яндекс.Практикуме
- токен телеграм-бота
- свой ID в телеграме


Запустить проект:

```
python homework.py
```
