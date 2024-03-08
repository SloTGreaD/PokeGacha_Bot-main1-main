
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import random
from info import helpinfo, rarity
import functions

# Загрузка токена из переменных окружения
TOKEN = functions.poke_bot_api
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

found_pokemon = []
class AsyncDatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_name)
        return await self.conn.cursor()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.commit()
        await self.conn.close()
class PokemonBot:

    def __init__(self):
        self.states = {}
        self.generator = None

    async def async_init(self):
        await functions.create_all_tables()

    async def start(self, message):
        await functions.add_user_to_number_of_pokemons(message.chat.id)
        await bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}!\nWelcome to Poké-Hunter. This bot allows you to search and catch Pokémons.\nPress /go to start your adventure.\nPress /help for more information.")


    async def handle_go_callback(self, call):
        chat_id = call.message.chat.id  # Для простоты предполагаем, что user_id и chat_id идентичны

        # Используйте `await` для асинхронного получения количества pokebols
        pokebol_count = await functions.pokebols_number(chat_id)

        if pokebol_count > 0:
            # Обработка нажатия кнопок "Go", "Keep going", "Skip"
            if call.data in ['go', 'keepgoing', 'skip']:
                found_pokemon.clear()
                try:
                    if call.data in ['keepgoing', 'skip']:
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                    if call.data == 'skip':
                        await bot.delete_message(call.message.chat.id, call.message.message_id-1)
                except Exception as e:
                    print(f"Ошибка при удалении сообщения: {e}")

                if random.choice([True, False]):
                    await self.show_catch_or_skip_buttons(chat_id, pokebol_count)
                else:
                    await self.back_to_start(chat_id, call.message.message_id)

            # Обработка нажатия кнопок "Catch", "Retry"
            elif call.data in ['catch', 'retry']:
                if call.data == 'retry':
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                if random.choice([True, False]):
                    
                    await self.show_captured_or_retry_buttons(chat_id, call.message.message_id)

                else:
                    
                    await self.show_captured_or_not_buttons(chat_id, call.message.message_id)


        else:
            await bot.send_message(chat_id, "У вас нет pokebol! Найдите или купите их, чтобы продолжить ловлю покемонов.")
            #на будущее: нужно придумать какое то продолжение для пользователя после этого сообщения




    async def show_go_buttons(self, chat_id):
        # Отправка кнопки "Go" для начала поиска покемона
        markup = types.InlineKeyboardMarkup()
        button_go = types.InlineKeyboardButton('Go', callback_data='go')
        markup.add(button_go)
        await bot.send_message(chat_id, "Press 'Go' to start searching for a Pokemon:", reply_markup=markup)

    async def back_to_start(self, chat_id, message_id):
        # Возвращение к начальному состоянию после неудачной попытки
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('Keep going', callback_data='keepgoing')
        markup.add(button_back)
        await bot.send_message(chat_id, 'You did not find anything', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)


    async def show_pokedex(self, chat_id):
        async for pokedex_page in functions.show_pokedex(chat_id):
            markup = types.InlineKeyboardMarkup()
            next_list = types.InlineKeyboardButton('Next', callback_data='next')
            markup.add(next_list)
            # Используйте pokedex_page для отправки текущего содержимого страницы
            await bot.send_message(chat_id, pokedex_page, reply_markup=markup)

    async def my_pokemons(self, chat_id):
        pokemons = await functions.my_pokemons(chat_id)
        # Проверка на пустую строку 'pokedex' перед отправкой
        if pokemons.strip() == '':
            await bot.send_message(chat_id, "No Pokemons have been captured yet.")
        else:
            await bot.send_message(chat_id, pokemons)



    async def show_catch_or_skip_buttons(self, chat_id, pokebol_count):
        # Отображение кнопок "Try to Catch" и "Skip" после успешной попытки
        markup = types.InlineKeyboardMarkup()
        button_catch = types.InlineKeyboardButton('Try to Catch', callback_data='catch')
        button_skip = types.InlineKeyboardButton('Skip', callback_data='skip')
        markup.add(button_catch, button_skip)
        

        # Отображение случайного покемона с весами
        chosen_pokemon, gen = functions.pokemon_catch() #функция с вероятностями выпадения покемонов в файле functions.py
        pokemon_image = f'images/{chosen_pokemon.capitalize()}.webp'
        with open(pokemon_image, 'rb') as pokemon_photo:
            found_pokemon.append(chosen_pokemon)
            sent_message = await bot.send_document(chat_id, pokemon_photo)
            gen_info = functions.generations[chosen_pokemon]
            if gen_info != '': gen_info = f' ({gen_info})'
            await bot.send_message(chat_id, f"You found a {chosen_pokemon}{gen_info}!\n\n It has '{gen}' rarity.\n\n What would you like to do?\n\nYou have {pokebol_count} pokebols",  reply_markup=markup)
            self.states[chat_id] = {'state': 'choose_catch_or_skip', 'message_id': sent_message.message_id, 'gen': gen}
            
            



    async def show_captured_or_retry_buttons(self, chat_id, message_id):
        # Отображение кнопки "Keep going" после успешного захвата
        gen = self.states[chat_id].get('gen', '')
        markup = types.InlineKeyboardMarkup()
        button_go = types.InlineKeyboardButton('Keep going', callback_data='go')
        markup.add(button_go)
        await functions.capture_pokemon(chat_id, f"{found_pokemon[0]}")
        await functions.capture_pokemon_by_rarity(chat_id, f"{found_pokemon[0]}", gen)
        
        await bot.send_message(chat_id, f"You captured a {found_pokemon[0]}!", reply_markup=markup)

        #bot.delete_message(chat_id, message_id)

    async def show_captured_or_not_buttons(self, chat_id, message_id):
        # Отображение кнопки "Try again" после неудачной попытки захвата
        markup = types.InlineKeyboardMarkup()
        button_try_again = types.InlineKeyboardButton('Try again', callback_data='retry')
        markup.add(button_try_again)
        await functions.capture_failed(chat_id)
        await bot.send_message(chat_id, 'Bad luck', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)

    async def get_pokebols(self, user_id):
        async with AsyncDatabaseConnection('pokedex.sql') as cur:
            can_get_pokebols = await functions.check_pokebols_elegibility(user_id) #возвращает True or False
            text = functions.time_until_next_midnight()
            if can_get_pokebols:
                await functions.add_pokebols(user_id, 50, cur)
                await bot.send_message(user_id, f'Вы получили 50 бесплатных покеболов. До следующего бесплатного получения осталось {text}')
            else:
                await bot.send_message(user_id, f'К сожалению вы еще не можете получить бесплатные покеболы. Дождитесь следующего дня. Осталось ждать: {text}')
        
    def run(self):
        # Запуск бота в режиме бесконечного опроса
        dp.infinity_polling()

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
        await pokemon_bot.start(message)

    @dp.message_handler(commands=['pokedex'])
    async def deploy_pokedex(message: types.Message):
        chat_id = message.chat.id
        await pokemon_bot.show_pokedex(chat_id)

    @dp.message_handler(commands=['go'])
    async def show_go_message(message: types.Message):
        chat_id = message.chat.id
        await pokemon_bot.show_go_buttons(chat_id)

    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message):
        await bot.send_message(message.chat.id, helpinfo, parse_mode='HTML')

    @dp.message_handler(commands=['get_pokebols'])
    async def get_pokebols_handler(message: types.Message):
        await pokemon_bot.get_pokebols(message.chat.id)

    @dp.message_handler(commands=['my_pokemons'])
    async def my_pokemons_handler(message: types.Message):
        await pokemon_bot.my_pokemons(message.chat.id)
    
    @dp.message_handler(commands=['rarity'])
    async def rarity_command(message: types.Message):
        await bot.send_message(message.chat.id, rarity, parse_mode='HTML')

    @dp.callback_query_handler(Text(equals="next"))
    async def scroll_to_next(call: types.CallbackQuery):
        markup = InlineKeyboardMarkup()
        next_list = InlineKeyboardButton('Next', callback_data='next')
        markup.add(next_list)
        try:
            await bot.edit_message_text(next(pokemon_bot.generator), call.message.chat.id, call.message.message_id, reply_markup=markup)
        except StopIteration:
            await bot.edit_message_text('This Pokedex is not valid anymore, press /pokedex to get up-to-date version', call.message.chat.id, call.message.message_id)

    @dp.callback_query_handler(Text(equals=['go', 'keepgoing', 'skip', 'retry', 'catch']))
    async def handle_go_callback_wrapper(call: types.CallbackQuery):
        await pokemon_bot.handle_go_callback(call)

    # Запуск бота
    asyncio.run(main())