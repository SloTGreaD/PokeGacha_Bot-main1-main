from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified, BadRequest, MessageToEditNotFound, MessageIdInvalid, MessageToDeleteNotFound
import asyncio
from class_reply import under_keyboard
import info
import functions
import energy
import regestration
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from class_PokemonBot import PokemonBot


# Загрузка токена из переменных окружения
from info import bot, dp
under_keyboard_class = under_keyboard()


users_bot: dict[int, PokemonBot] = {}

class Form(StatesGroup):
    waiting_for_nickname = State()
class Form1(StatesGroup):
    waiting_for_nickname = State()  # Существующее состояние для регистрации никнейма
    changing_nickname = State()

async def main():
    try:
        await functions.create_all_tables()
        try:
            await dp.start_polling()
        except Exception as e:
            print(e)
    finally:
        await bot.session.close()


async def create_bot_class_for_user(user_id):
    global users_bot
    if user_id not in users_bot:
        users_bot[user_id] = PokemonBot()


if __name__ == "__main__":
    # Создание экземпляра класса PokemonBot
    pokemon_bot = PokemonBot()
    # Обработчики сообщений и колбеков
    @dp.message_handler(commands=['start'])
    async def start_wrapper(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        if await regestration.check_user_nickname(user_id):
            # Пользователь уже зарегистрирован, продолжаем обычную логику
            await message.reply("Добро пожаловать обратно! Вы уже зарегистрированы.")
            await create_bot_class_for_user(chat_id)
            await users_bot[chat_id].start(message)
        else:
            # Пользователь не зарегистрирован, запрашиваем никнейм
            await message.reply("Похоже, вы здесь впервые! Пожалуйста, введите ваш никнейм для регистрации.")
            await Form.waiting_for_nickname.set()
        
    @dp.message_handler(state=Form.waiting_for_nickname)
    async def process_nickname(message: types.Message, state: FSMContext):
        nickname = message.text
        user_id = message.from_user.id
        chat_id = message.chat.id
        # Проверка, занят ли никнейм
        if await regestration.is_nickname_taken(nickname):
            await message.reply("Этот никнейм уже занят. Пожалуйста, выберите другой.")
        else:
            await regestration.register_new_user(user_id, nickname)
            await message.reply("Вы успешно зарегистрированы!")
            await state.finish()
            await create_bot_class_for_user(chat_id)
            await users_bot[chat_id].start(message)

    @dp.message_handler(commands=['📱Pokedex'])
    async def deploy_pokedex(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].show_pokedex_variations(chat_id, "Select what do you want to see in Pokédex")


    @dp.message_handler(commands=['🏃‍♂️Start_Adventure'])
    async def show_go_message(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        user_bot = users_bot[chat_id]
        user_bot.sleeping_task = asyncio.create_task(user_bot.start_adventure(chat_id))
    
    @dp.message_handler(commands=['🔚End_Adventure'])
    async def show_menu_message(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        try:
            users_bot[chat_id].sleeping_task.cancel()
        except AttributeError:
            await users_bot[chat_id].end_adventure_manually(chat_id)


    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message):
        await bot.send_message(message.chat.id, info.HelpInfo, parse_mode='HTML')


    @dp.message_handler(commands=['🔴⚪Get_Pokebolls'])
    async def get_pokebols_handler(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].get_pokebols(chat_id)


    @dp.message_handler(commands=['have_a_rest'])
    async def get_energy_handler(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].gain_energy(message.chat.id)


    @dp.message_handler(commands=['🎒My_pokemons'])
    async def my_pokemons_handler(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        keyboard = users_bot[chat_id].my_pokemons_keyboard()
        await message.answer("Выберите, как вы хотите просмотреть своих покемонов:", reply_markup=keyboard)
    

    @dp.message_handler(commands=['🍽️Meal'])
    async def items_handler(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].items_buttons(message.chat.id)
    
    @dp.message_handler(commands=['📋Profile'])
    async def profile_handler(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].profile_button(message.chat.id)

    @dp.message_handler(commands=['rarity'])
    async def rarity_command(message: types.Message):
        await bot.send_message(message.chat.id, info.RARITY, parse_mode='HTML')

    @dp.message_handler(commands=['📝Change_Nickname'])
    async def profile(call: types.CallbackQuery):
        markup = await under_keyboard_class.cancel_change_nickname()
        # Отправляем дополнительное сообщение для ввода нового никнейма
        await bot.send_message(call.from_user.id, "Пожалуйста, введите новый никнейм:", reply_markup=markup)
    
        # Устанавливаем состояние для ожидания нового никнейма
        await Form1.changing_nickname.set()
    
    @dp.message_handler(commands=['🏠Main_Menu'])
    async def main_menu(message: types.Message):
        markup = await under_keyboard_class.back_to_menu()
        await bot.send_message(message.chat.id, 'Going to Menu', reply_markup=markup)
    
    @dp.message_handler(Text(startswith="/"), state=Form1.changing_nickname)
    async def skip_command(message: types.Message, state: FSMContext):
        # Можно просто игнорировать сообщение или напомнить, что ожидается никнейм
        await message.reply("Пожалуйста, введите никнейм, а не команду.")

    @dp.message_handler(commands=['❌Discard_Changes'], state="*")
    async def discard_changes(message: types.Message, state: FSMContext):
        markup = await under_keyboard_class.profile_menu()
        await message.reply('Изменения отменены❌', reply_markup=markup)
        await state.finish()

    @dp.message_handler(lambda message: not message.text.startswith('/'), state=Form1.changing_nickname)
    async def change_nickname(message: types.Message, state: FSMContext):
        new_nickname = message.text.strip()
        user_id = message.from_user.id

        if new_nickname.startswith('/'):
            await message.reply("Никнейм не должен начинаться с символа '/'. Пожалуйста, выберите другой никнейм.")
            return

        if await regestration.is_nickname_taken(new_nickname):
            await message.reply("Этот никнейм уже занят. Пожалуйста, выберите другой.")
            return

        await regestration.update_nickname(user_id, new_nickname)
        markup = await under_keyboard_class.profile_menu()
        await message.reply("Ваш никнейм успешно изменён.", reply_markup=markup)
        await state.finish()


    @dp.callback_query_handler(Text(equals='🖼️pictures')) #🖼️
    async def see_in_pictures(message: types.Message):
        chat_id = message.chat.id
        await create_bot_class_for_user(chat_id)
        markups = await users_bot[chat_id].command_markups('pictures')
        await bot.send_message(message.chat.id, "Choose the rarity you want to see", reply_markup=markups)

    @dp.callback_query_handler(lambda c: c.data == 'view_list')
    async def show_pokemon_list(callback_query: types.CallbackQuery):
        chat_id = callback_query.message.chat.id
        await create_bot_class_for_user(chat_id)
        message_id = callback_query.message.message_id
        await bot.delete_message(chat_id, message_id)
        await users_bot[chat_id].show_my_pokemons_variations(chat_id)
        await bot.answer_callback_query(callback_query.id)  ##?????????

    @dp.callback_query_handler(lambda c: c.data == 'view_photos')
    async def show_pokemon_photos(callback_query: types.CallbackQuery):
        chat_id = callback_query.message.chat.id
        await create_bot_class_for_user(chat_id)
        message_id = callback_query.message.message_id
        await bot.delete_message(chat_id, message_id)
        markups = await users_bot[chat_id].command_markups('pictures')
        await bot.send_message(callback_query.message.chat.id, "Choose the rarity you want to see", reply_markup=markups)
        


    @dp.callback_query_handler(Text(equals="next"))
    async def scroll_to_next(call: types.CallbackQuery):
        markup = InlineKeyboardMarkup()
        next_list = InlineKeyboardButton('Next', callback_data='next')
        markup.add(next_list)
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        try:
            text = await users_bot[chat_id].generator.__anext__()
            await bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        except AttributeError:
            await bot.edit_message_text('This Item is not valid anymore, \npress /📱Pokedex to get up-to-date version',
                                        chat_id, call.message.message_id)
        except MessageNotModified:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id)



    @dp.callback_query_handler(Text(equals="All_pokedex"))
    async def show_allpokedex(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].show_all_pokedex(chat_id, call.message.message_id)


    @dp.callback_query_handler(Text(equals="All_pokemons"))
    async def show_all_my_pokemons(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].my_pokemons_all(chat_id, call.message.message_id)


    @dp.callback_query_handler(Text(endswith='_pokedex'))
    async def show_rariry_pokedex(call):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        markup = await users_bot[chat_id].command_markups('pokedex')
        try:
            await bot.edit_message_text(await functions.show_pokedex_rarity(chat_id, call.data[:-8]), chat_id, call.message.message_id, reply_markup=markup)
        except MessageNotModified:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id)

    @dp.callback_query_handler(Text(endswith='_pokemons'))
    async def show_rarity_pokemons(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        markup = await users_bot[chat_id].command_markups('pokemons')
        try:
            await bot.edit_message_text(await functions.show_pokemons_rarity(chat_id, call.data[:-9]), chat_id, call.message.message_id, reply_markup=markup)
        except MessageNotModified:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id)

    @dp.callback_query_handler(Text(endswith='_pictures'))
    async def show_rarity_pictures(call):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        try:
            await users_bot[chat_id].show_first_pokemon_picture(chat_id, call.message.message_id, call.data[:-9])
        except MessageToDeleteNotFound:
            pass


    @dp.callback_query_handler(Text(equals='forward'))
    async def change_pokemon_picture(call):
        chat_id = call.message.chat.id
        try:
            await users_bot[chat_id].increase_and_show_pokemon_picture(call.message.chat.id, call.message.message_id, 1)
        except MessageNotModified:
            pass
        except BadRequest:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id, "❗❗❗Please slow down, bot cannot process quick button presses❗❗❗")

    @dp.callback_query_handler(Text(equals='back'))
    async def change_pokemon_picture(call):
        chat_id = call.message.chat.id
        try:
            await users_bot[chat_id].decrease_and_show_pokemon_picture(chat_id, call.message.message_id, 1)
        except MessageNotModified:
            pass
        except BadRequest:
            await bot.send_message(chat_id, "Please slow down, bot cannot process quick button presses")


    @dp.callback_query_handler(Text(equals='go_back'))
    async def go_to_pictures_start(call):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        await bot.delete_message(chat_id, call.message.message_id)
        markups = await users_bot[chat_id].command_markups('pictures')
        await bot.send_message(chat_id, "Choose the rarity you want to see", reply_markup=markups)

    @dp.callback_query_handler(Text(equals=['Go', 'keepgoing', 'skip', 'retry', 'catch']))
    async def handle_go_callback_wrapper(call: types.CallbackQuery):
        markup = types.InlineKeyboardMarkup()
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        try:
            await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=markup)
            await users_bot[chat_id].handle_go_callback(call)
        except MessageToEditNotFound:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id)
        except MessageNotModified:
            await users_bot[chat_id].slow_down_message(chat_id, call.message.message_id)
        except MessageIdInvalid:
            await users_bot[chat_id].slow_down_message(chat_id)
        except MessageToDeleteNotFound: #значит приключение закончилось
            pass

    @dp.callback_query_handler(
        Text(equals=['check_bread', 'check_rice', 'check_ramen', 'check_spaghetti']))  # обрабатывает колбэк
    async def handle_check_bread(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        await users_bot[chat_id].item_handler(call)  # использует хлеб

    @dp.callback_query_handler(lambda c: c.data == 'use_candy')
    async def use_candy(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        await create_bot_class_for_user(chat_id)
        result = await users_bot[chat_id].candy_button(call)  # Вызов метода, который проверяет и использует Candy
        if result:
            # Увеличиваем счетчик использований "Candy" на 1 или инициализируем его, если не было использований
            users_bot[chat_id].candy_usage += 1
        
    

    # Запуск бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
