r"""
.
С наступающим Новым Годом!

           *             ,
                       _/^\_
                      <     >
     *                 /.-.\         *
              *        `/&\`                   *
                      ,@.*;@,
                     /_o.I %_\    *
        *           (`'--:o(_@;
                   /`;--.,__ `')             *
                  ;@`o % O,*`'`&\
            *    (`'--)_@ ;o %'()\      *
                 /`;--._`''--._O'@;
                /&*,()~o`;-.,_ `""`)
     *          /`,@ ;+& () o*`;-';\
               (`""--.,_0 +% @' &()\
               /-.,_    ``''--....-'`)  *
          *    /@%;o`:;'--,.__   __.'\
              ;*,&(); @ % &^;~`"`o;@();         *
              /(); o^~; & ().o@*&`;&%O\
              `"="==""==,,,.,="=="==="`
           __.----.(\-''#####---...___...-----._
         '`         \)_`
                 .--' ')
               o(  )_-\
                 `""

"""

import exceptions
import logging
import os
import requests
import sys
import telegram
import time
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

PRACTICUM_TOKEN = os.getenv('YA_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGA_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGA_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
HW_TIME_DEPTH = (60 * 60 * 24 * 30)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка доступности переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info(f'Начало отправки сообщения: {message} в Telegram.')
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f'<b><i>{message}</i></b>',
            parse_mode=telegram.ParseMode.HTML
        )
    except telegram.error.TelegramError as error:
        logger.error(
            f'Ошибка отправки сообщения: {error}'
        )
        raise exceptions.SendMessageError(
            f'Ошибка отправки сообщения: {error}'
        )
    else:
        logging.debug(f'Успешная отправка сообщения: "{message}"')


def get_api_answer(timestamp):
    """
    Делает запрос к единственному эндпоинту API-сервиса.
    В качестве параметра в функцию передается временная метка.
    В случае успешного запроса должна вернуть ответ API,
    приведя его из формата JSON к типам данных Python.
    """
    api_dict = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': timestamp}
    }
    try:
        logging.info(f"Начало запроса к эндпоинту : {api_dict['url']}")
        homework_statuses = requests.get(**api_dict)
        if homework_statuses.status_code != HTTPStatus.OK:
            raise exceptions.ApiRequestError(
                f"Ошибка соединения с эндпоинтом: {api_dict['url']}"
            )
        return homework_statuses.json()
    except requests.RequestException as error:
        raise exceptions.RequestError(f'Ошибка запроса: {error}')


def check_response(response):
    """
    Проверяет ответ API на соответствие документации.
    В качестве параметра функция получает ответ API,
    приведенный к типам данных Python.
    """
    if not isinstance(response, dict) or 'homeworks' not in response:
        raise TypeError('В ответе API нет словаря c домашками')
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError("Oтвет по ключу 'homeworks' не возвращает список")
    return homeworks[0]['status']


def parse_status(homework):
    """
    Извлекает домашней работы.
    В качестве параметра функция получает только один элемент
    из списка домашних работ.
    Возвращает подготовленную для отправки в Telegram строку.
    """
    if 'homework_name' not in homework:
        raise KeyError("В ответе API отсутствует ключ 'homework_name'")
    status = homework['status']
    if status == 'unknown':
        raise exceptions.HwStatusUnknown('Статус домашки не задокументирован')
    verdict = HOMEWORK_VERDICTS[status]
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неидентифицированный статус: {status}')
    homework_name = homework['homework_name']
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """
    Основная логика работы бота.
    1 - Сделать запрос к API.
    2 - Проверить ответ.
    3 - Если есть обновления — получить статус работы из обновления
        и отправить сообщение в Telegram.
    4 - Подождать некоторое время и вернуться в пункт 1.
    """
    if not check_tokens():
        logging.critical('Отсутсвуют переменные окружения')
        sys.exit('Бот так не будет работать, нужны переменные окружения.')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time()) - HW_TIME_DEPTH

    status = ''
    error_msg = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            get_status = check_response(response)
            if status == get_status:
                logger.debug('Статус как прежде')
            else:
                status = get_status
                text = parse_status(response['homeworks'][0])
                send_message(bot, text)
        except Exception as error:
            if error_msg != error:
                error_msg = error
                message = f'Сбой в работе программы: {error_msg}'
                send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
