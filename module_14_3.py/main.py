from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Рассчитать'),
            KeyboardButton(text = 'Информация')
        ],
        [KeyboardButton(text = 'Купить')]
    ], resize_keyboard = True
)

check_menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data = "calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data = "formulas")]
    ]
)



buy_menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Product1", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product2", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product3", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product4", callback_data = "product_buying")]
    ]
)
#buy_menu.add(button)
#buy_menu.add(button2)
#buy_menu.add(button3)
#buy_menu.add(button4)
@dp.message_handler(commands= ['start'])
async def start(message):
    await message.answer(f"Привет! Я бот помогающий твоему здоровью",reply_markup = start_menu)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('1.jpg',"rb")as img:
        await message.answer_photo(img,f"Название: Product1/Описание jpg:/Цена:{1*800}",reply_markup=start_menu)
    with open('2.jpg', "rb") as img:
        await message.answer_photo(img,f"Название: Product2/Описание jpg:/Цена:{2*1000}",reply_markup=start_menu)
    with open('3.jpg', "rb") as img:
        await message.answer_photo(img,f"Название: Product3/Описание jpg:/Цена:{3*750}",reply_markup=start_menu)
    with open('4.png', "rb") as img:
        await message.answer_photo(img,f"Название: Product4/Описание png:/Цена:{4*700}",reply_markup=start_menu)
        await message.answer(f" Выберите продукт для покупки:",reply_markup=buy_menu)

#@dp.message_handler(text="buy_menu")
#async def info(message):
    #await message.answer("Выберите продукт для покупки:",reply_markup=buy_menu)
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выбери опцию:",reply_markup=check_menu)

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer("10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) - 161")
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
    await call.answer()
@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Ваша норма калорий {calories_wom}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)