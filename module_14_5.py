from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
data = get_all_products()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_4 = KeyboardButton(text='Регистрация')
kb.add(button_1)
kb.add(button_2)
kb.add(button_3)
kb.add(button_4)


ikb = InlineKeyboardMarkup()
ibutton_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ibutton_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.add(ibutton_1)
ikb.add(ibutton_2)

ikb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ])


@dp.message_handler(commands=['start'])
async def all_massages(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    user_name = await state.get_data()
    user_name = user_name['username']
    check = is_included(user_name)
    if check:
        await message.answer(text='Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer(text='Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(text='Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    add_user(user_data['username'], user_data['email'], user_data['age'])
    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 (для мужчин)')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(text='Введите свой возраст в годах:')
    await UserState.age.set()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=ikb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for j in data:
        await message.answer(text=f'Название: {str(j[1])} | Описание: {str(j[2])} | Цена: {str(j[3])}',)
        with open(f'{str(j[0])}.jpg', 'rb') as img:
           await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки:', reply_markup=ikb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
            

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост в см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    Calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age'])
    await message.answer(Calories)
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
