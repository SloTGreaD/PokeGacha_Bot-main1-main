from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from class_reply import under_keyboard
import info
import functions
import energy
import regestration
from class_PokemonBot import PokemonBot
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


# Загрузка токена из переменных окружения
from info import bot, dp
under_keyboard_class = under_keyboard()

class Form(StatesGroup):
    waiting_for_nickname = State()

async def main():
    try:
        pokemon_bot = PokemonBot()
        await pokemon_bot.async_init()
        await dp.start_polling()
    finally:
        await bot.session.close()


# Если файл запущен напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    # Создание экземпляра класса PokemonBot
    pokemon_bot = PokemonBot()


    # Обработчики сообщений и колбеков
    @dp.message_handler(commands=['start'])
    async def start_wrapper(message: types.Message):
        user_id = message.from_user.id
        if await regestration.check_user_nickname(user_id):
            # Пользователь уже зарегистрирован, продолжаем обычную логику
            await message.reply("Добро пожаловать обратно! Вы уже зарегистрированы.")
            await pokemon_bot.start(message)
        else:
            # Пользователь не зарегистрирован, запрашиваем никнейм
            await message.reply("Похоже, вы здесь впервые! Пожалуйста, введите ваш никнейм для регистрации.")
            await Form.waiting_for_nickname.set()

        
    @dp.message_handler(state=Form.waiting_for_nickname)
    async def process_nickname(message: types.Message, state: FSMContext):
        nickname = message.text
        user_id = message.from_user.id
        await regestration.register_new_user(user_id, nickname)
        await message.reply("Вы успешно зарегистрированы!")
        await state.finish()
        await pokemon_bot.start(message)

    @dp.message_handler(commands=['📱Pokedex'])
    async def deploy_pokedex(message: types.Message):
        chat_id = message.chat.id
        await pokemon_bot.show_pokedex_variations(chat_id, "Select what do you want to see in Pokédex")


    @dp.message_handler(commands=['🏃‍♂️Start_Adventure'])
    async def show_go_message(message: types.Message):
        chat_id = message.chat.id
        await pokemon_bot.gain_energy_at_start(chat_id)
        await pokemon_bot.show_go_buttons(chat_id)
    
    @dp.message_handler(commands=['🔚End_Adventure'])
    async def show_menu_message(message: types.Message):
        
        await pokemon_bot.del_last_go_message(message)


    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message):
        await bot.send_message(message.chat.id, info.HelpInfo, parse_mode='HTML')


    @dp.message_handler(commands=['🔴⚪Get_Pokebolls'])
    async def get_pokebols_handler(message: types.Message):
        await pokemon_bot.get_pokebols(message.chat.id)


    @dp.message_handler(commands=['have_a_rest'])
    async def get_energy_handler(message: types.Message):
        await pokemon_bot.gain_energy(message.chat.id)


    @dp.message_handler(commands=['🎒My_pokemons'])
    async def my_pokemons_handler(message: types.Message):
        keyboard = pokemon_bot.my_pokemons_keyboard()
        await message.answer("Выберите, как вы хотите просмотреть своих покемонов:", reply_markup=keyboard)
    

    @dp.message_handler(commands=['🍽️Meal'])
    async def items_handler(message: types.Message):
        await pokemon_bot.items_buttons(message.chat.id)


    @dp.message_handler(commands=['rarity'])
    async def rarity_command(message: types.Message):
        await bot.send_message(message.chat.id, info.RARITY, parse_mode='HTML')


    @dp.callback_query_handler(Text(equals='🖼️pictures')) #🖼️
    async def see_in_pictures(message: types.Message):
        markups = await pokemon_bot.command_markups('pictures')
        await bot.send_message(message.chat.id, "Choose the rarity you want to see", reply_markup=markups)

    @dp.callback_query_handler(lambda c: c.data == 'view_list')
    async def show_pokemon_list(callback_query: types.CallbackQuery):
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        await bot.delete_message(chat_id, message_id)
        await pokemon_bot.show_my_pokemons_variations(callback_query.message.chat.id)
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data == 'view_photos')
    async def show_pokemon_photos(callback_query: types.CallbackQuery):
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        await bot.delete_message(chat_id, message_id)
        markups = await pokemon_bot.command_markups('pictures')
        await bot.send_message(callback_query.message.chat.id, "Choose the rarity you want to see", reply_markup=markups)
        


    @dp.callback_query_handler(Text(equals="next"))
    async def scroll_to_next(call: types.CallbackQuery):
        markup = InlineKeyboardMarkup()
        next_list = InlineKeyboardButton('Next', callback_data='next')
        markup.add(next_list)
        try:
            text = await pokemon_bot.generator.__anext__()
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        except StopIteration:
            await bot.edit_message_text('This Item is not valid anymore, press /📱Pokedex to get up-to-date version',
                                        call.message.chat.id, call.message.message_id)
        except MessageNotModified:
            pass


    @dp.callback_query_handler(Text(equals="All_pokedex"))
    async def show_allpokedex(call: types.CallbackQuery):
        await pokemon_bot.show_all_pokedex(call.message.chat.id, call.message.message_id)


    @dp.callback_query_handler(Text(equals="All_pokemons"))
    async def show_all_my_pokemons(call: types.CallbackQuery):
        await pokemon_bot.my_pokemons_all(call.message.chat.id, call.message.message_id)


    @dp.callback_query_handler(Text(endswith='_pokedex'))
    async def show_rariry_pokedex(call):
        chat_id = call.message.chat.id
        markup = await pokemon_bot.command_markups('pokedex')
        await bot.edit_message_text(await functions.show_pokedex_rarity(chat_id, call.data[:-8]), chat_id,
                                    call.message.message_id, reply_markup=markup)


    @dp.callback_query_handler(Text(endswith='_pokemons'))
    async def show_rarity_pokemons(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        markup = await pokemon_bot.command_markups('pokemons')
        await bot.edit_message_text(await functions.show_pokemons_rarity(chat_id, call.data[:-9]), chat_id,
                                    call.message.message_id, reply_markup=markup)


    @dp.callback_query_handler(Text(endswith='_pictures'))
    async def show_rarity_pictures(call):
        await pokemon_bot.show_first_pokemon_picture(call.message.chat.id, call.message.message_id, call.data[:-9])


    @dp.callback_query_handler(Text(equals='forward'))
    async def change_pokemon_picture(call):
        try:
            await pokemon_bot.increase_and_show_pokemon_picture(call.message.chat.id, call.message.message_id, 1)
        except MessageNotModified:
            pass


    @dp.callback_query_handler(Text(equals='back'))
    async def change_pokemon_picture(call):
        chat_id = call.message.chat.id
        try:
            await pokemon_bot.decrease_and_show_pokemon_picture(chat_id, call.message.message_id, 1)
        except MessageNotModified:
            pass

    @dp.callback_query_handler(Text(equals='go_back'))
    async def go_to_pictures_start(call):
        chat_id = call.message.chat.id
        await bot.delete_message(chat_id, call.message.message_id)
        markups = await pokemon_bot.command_markups('pictures')
        await bot.send_message(chat_id, "Choose the rarity you want to see", reply_markup=markups)

    @dp.callback_query_handler(Text(equals=['🏃‍♂️Start_Adventure', 'keepgoing', 'skip', 'retry', 'catch']))
    async def handle_go_callback_wrapper(call: types.CallbackQuery):
        markup = types.InlineKeyboardMarkup()
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        await pokemon_bot.handle_go_callback(call)


    @dp.callback_query_handler(
        Text(equals=['check_bread', 'check_rice', 'check_ramen', 'check_spaghetti']))  # обрабатывает колбэк
    async def handle_check_bread(call: types.CallbackQuery):
        await pokemon_bot.item_handler(call)  # использует хлеб

    @dp.callback_query_handler(lambda c: c.data == 'use_candy')
    async def use_candy(call: types.CallbackQuery):
        user_id = call.message.chat.id
        chat_id = call.message.chat.id
        result = await pokemon_bot.candy_button(call)  # Вызов метода, который проверяет и использует Candy
        if result:
            # Увеличиваем счетчик использований "Candy" на 1 или инициализируем его, если не было использований
            pokemon_bot.candy_usage[chat_id] = pokemon_bot.candy_usage.get(chat_id, 0) + 1
            
        


    # Запуск бота
    asyncio.run(main())
