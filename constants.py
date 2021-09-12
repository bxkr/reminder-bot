from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot

SCHEDULE_SCRIPT = 'schedule.py'
TOKEN_FILE = 'token.txt'
DATABASE = 'database.json'
INTERPRETER_FILE = 'py'

API_TOKEN = open(TOKEN_FILE, 'r').read()
BOT = Bot(token=API_TOKEN)
HELLO = 'Приветик.\n\n' \
        'Ты можешь нажать на кнопку, чтобы добавить бота в чат.\n' \
        'Дальнейшее управление ботом может осуществляться в чате.'
ADD_BOT = 'Добавить бота в беседу'
CONGRATS = 'Бот успешно добавлен. Вы можете управлять им кнопками ниже. (это меню можно также вызвать с помощью ' \
           '/settings) '
SETTINGS = 'Вы в настройках. Выберите, что вы хотите изменить/посмотреть с помощью кнопок ниже.'
TIME_SET = 'Время'
DAYS = 'Дни недели'
MESSAGE_SET = 'Текст'
ENTER_NEW_TIME = 'Текущее время отправки: {0}.\nИзменить время: /set_time \'ЧЧ:ММ\'.'
ENTER_NEW_MESSAGE = 'Текущее отправляемое сообщение: \'{}\'\nИзменить сообщение: /set_message СООБЩЕНИЕ.'
TIME_FORMAT = '\'{}\' не соответствует формату \'ЧЧ:ММ\'!'
TIME_EMPTY = 'Вы не указали время!'
TIME_OK = 'Время успешно установлено! Новое время отправки: {}'
MESSAGE_EMPTY = 'Вы не указали сообщение!'
MESSAGE_OK = 'Сообщение успешно установлено! Новое сообщение: \'{}\''
DAYS_SET = 'Управляйте днями отправки с помощью inline-кнопок ниже.'
DAYS_LIST = 'Пн,Вт,Ср,Чт,Пт,Сб,Вс'.split(',')
RETRY_AFTER = 'Вы слишком часто используете кнопки. Нажмите снова через {} секунд.'
SETTINGS_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=
                                         [[InlineKeyboardButton(TIME_SET, callback_data='time-set'),
                                           InlineKeyboardButton(MESSAGE_SET, callback_data='message-set'),
                                           InlineKeyboardButton(DAYS, callback_data='days-set')],
                                          [InlineKeyboardButton('Закрыть', callback_data='close')]])
BACK_BUTTON = [InlineKeyboardButton('🔄 Обновить', callback_data='refresh'),
               InlineKeyboardButton('✔ Вернуться', callback_data='back')]
BACK_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[BACK_BUTTON])
CLOSE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton('Закрыть', callback_data='close')]])
HAVE_A_GREAT_DAY = 'Удачного дня! :)'
DEFAULT_MESSAGE = 'Обыкновенное сообщение'
DEFAULT_TIME = 'datetime.time(hour=14, minute=3)'
ALREADY_ADDED = 'Бот уже добавлен.\n\n' + SETTINGS
REFRESHING = 'Обновление...'
PRIMARY_TIME_FORMAT = '%H:%M'

def add_bot_keyboard(link): return [[InlineKeyboardButton(ADD_BOT, url=link)]]


def days_set_keyboard(days):
    i = 0
    row1, row2 = [], []
    for is_active in days:
        if is_active:
            sym = '✅'
        else:
            sym = '❎'
        if i >= 3:
            row2.append(InlineKeyboardButton(text=f'{sym} {DAYS_LIST[i]}', callback_data=f'toggle-day{i}'))
        else:
            row1.append(InlineKeyboardButton(text=f'{sym} {DAYS_LIST[i]}', callback_data=f'toggle-day{i}'))
        i += 1
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, BACK_BUTTON])
