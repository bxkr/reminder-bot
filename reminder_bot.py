import asyncio
import datetime
import logging

from aiogram import Dispatcher, executor, filters, exceptions
from aiogram.utils.deep_linking import get_startgroup_link

from constants import *
from database import Data

from subprocess import Popen as Prompt
from json import loads as jload
from os.path import exists

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(BOT)
processes = []


def marking_up(callback: types.CallbackQuery):
    data = Data(callback.message.chat.id)
    day = int(callback.data[len(callback.data) - 1])
    result = data.days
    result[day] = not result[day]
    data.days = result
    return days_set_keyboard(data.days)


@dp.message_handler(filters.CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def start_private(message: types.Message):
    link = await get_startgroup_link('stay-alive')
    await message.answer(HELLO, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=add_bot_keyboard(link)))


@dp.message_handler(filters.CommandStart(), filters.Regexp('stay-alive'), FILTER_GROUP_OR_SUPERGROUP)
async def start_chat(message: types.Message):
    with open(DATABASE, 'r+') as db:
        dict_f = jload(db.read())
        if str(message.chat.id) in dict_f.keys():
            Data(message.chat.id)
            await message.answer(ALREADY_ADDED, reply_markup=SETTINGS_KEYBOARD)
        else:
            data = Data(message.chat.id)
            t = eval(data.time).strftime(PRIMARY_TIME_FORMAT)
            processes.append(Prompt([INTERPRETER_FILE, SCHEDULE_SCRIPT, t, str(message.chat.id)]))
            await message.answer(CONGRATS, reply_markup=SETTINGS_KEYBOARD)


@dp.callback_query_handler(filters.Regexp('time-set'))
async def time_set(callback: types.CallbackQuery):
    data = Data(callback.message.chat.id)
    try:
        await callback \
            .message.edit_text(ENTER_NEW_TIME.format(eval(data.time).strftime(PRIMARY_TIME_FORMAT)), reply_markup=BACK_KEYBOARD)
        await callback.answer()
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('message-set'))
async def message_set(callback: types.CallbackQuery):
    data = Data(callback.message.chat.id)
    try:
        await callback.message.edit_text(ENTER_NEW_MESSAGE.format(data.message), reply_markup=BACK_KEYBOARD)
        await callback.answer()
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('days-set'))
async def days_set(callback: types.CallbackQuery):
    data = Data(callback.message.chat.id)
    try:
        await callback.message.edit_text(DAYS_SET, reply_markup=days_set_keyboard(data.days))
        await callback.answer()
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('toggle-day()'))
async def message_set(callback: types.CallbackQuery):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(marking_up(callback))
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('close'))
async def message_set(callback: types.CallbackQuery):
    try:
        await callback.answer(HAVE_A_GREAT_DAY)
        await callback.message.delete()
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('back'))
async def back(callback: types.CallbackQuery):
    try:
        await callback.answer()
        await callback.message.edit_text(
            SETTINGS, reply_markup=SETTINGS_KEYBOARD)
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.callback_query_handler(filters.Regexp('refresh'))
async def refresh(callback: types.CallbackQuery):
    data = Data(callback.message.chat.id)
    try:
        await callback.answer()
        message = callback.message.text
        if 'время' in message:
            await callback.message.edit_text(REFRESHING)
            await asyncio.sleep(.2)
            await callback.message. \
                edit_text(ENTER_NEW_TIME.format(eval(data.time).strftime(PRIMARY_TIME_FORMAT)), reply_markup=BACK_KEYBOARD)
        elif 'сообщение' in message:
            await callback.message.edit_text(REFRESHING)
            await asyncio.sleep(.2)
            await callback.message.edit_text(ENTER_NEW_MESSAGE.format(data.message), reply_markup=BACK_KEYBOARD)
    except exceptions.RetryAfter as exc:
        await callback.answer(RETRY_AFTER.format(exc.timeout))


@dp.message_handler(filters.CommandSettings(), FILTER_GROUP_OR_SUPERGROUP)
async def settings(message: types.Message):
    await message.answer(SETTINGS, reply_markup=SETTINGS_KEYBOARD)


@dp.message_handler(filters.Command('set_time'), FILTER_GROUP_OR_SUPERGROUP)
async def set_time(message: types.Message):
    data = Data(message.chat.id)
    if message.get_args() != '':
        try:
            temporary_time = datetime.datetime.strptime(message.get_args(), PRIMARY_TIME_FORMAT)
            data.time = f'datetime.time(hour={temporary_time.hour}, minute={temporary_time.minute})'
            for proc in processes:
                if proc.args[3] == str(message.chat.id):
                    proc.kill()
                    processes.append(Prompt([INTERPRETER_FILE, SCHEDULE_SCRIPT, message.get_args(), str(message.chat.id)]))
                    break
            await message.answer(TIME_OK.format(eval(data.time).strftime(PRIMARY_TIME_FORMAT)), reply_markup=CLOSE_KEYBOARD)
        except ValueError:
            await message.answer(TIME_FORMAT.format(message.get_args()), reply_markup=CLOSE_KEYBOARD)
    else:
        await message.reply(TIME_EMPTY, reply_markup=CLOSE_KEYBOARD)


@dp.message_handler(filters.Command('set_message'), FILTER_GROUP_OR_SUPERGROUP)
async def set_message(message: types.Message):
    data = Data(message.chat.id)
    if message.get_args() != '':
        data.message = message.get_args()
        await message.answer(MESSAGE_OK.format(data.message), reply_markup=CLOSE_KEYBOARD)
    else:
        await message.reply(MESSAGE_EMPTY, reply_markup=CLOSE_KEYBOARD)


if __name__ == '__main__':
    if not exists(DATABASE):
        with open(DATABASE, 'w') as start_new_file:
            start_new_file.write('{}')
    with open(DATABASE, 'r+') as start_db:
        start_dict_f = jload(start_db.read())
        for start_chat_id in start_dict_f.keys():
            start_chat_data = start_dict_f[start_chat_id]
            start_mt = eval(start_chat_data['time']).strftime(PRIMARY_TIME_FORMAT)
            processes.append(Prompt([INTERPRETER_FILE, SCHEDULE_SCRIPT, start_mt, start_chat_id]))
    executor.start_polling(dispatcher=dp, skip_updates=True)