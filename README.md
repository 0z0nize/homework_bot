![233348780-313ad8af-8fa5-47e0-x8cvfd1c-7f0aea8c24a122](https://user-images.githubusercontent.com/112638163/234632117-c09cbbb2-0453-4f23-b49a-480af6e9d3b5.png)

### Описание

Telegram-бот, который будет обращается к API сервиса Практикум.Домашка и узнаёт статус домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Бот умеет:
* раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
* при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
* логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

### Технологии:
![python version](https://img.shields.io/badge/Python-3.9.10-green?logo=python)
![Python version](https://img.shields.io/badge/dotenv-0.19.0-green?logo=dotenv)
![Python version](https://img.shields.io/badge/telegrambot-13.7-green?logo=telegram)

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

##### Автор проекта:
##### [_Владислав Шкаровский_](https://github.com/0z0nize)
