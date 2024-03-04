import telebot
from telebot import types
import random
import functions
import sqlite3
from functions import DatabaseConnection
from info import helpinfo
from info import rarity

# Загрузка токена из переменных окружения
bot = telebot.TeleBot(functions.poke_bot_api)

found_pokemon = []


class PokemonBot:


    def __init__(self):
        # Словарь для хранения состояний пользователей
        self.states = {}
        self.generator = None
        # Создаем таблицу для спойманных покемонов
        functions.create_all_tables()

    def start(self, message):

        functions.add_user_to_number_of_pokemons(message.chat.id) #добавляет только новых юзеров
        # Приветственное сообщение при старте
        bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}!\nWelcome to Poké-Hunter. This bot allows you to search and catch Pokémons.\nPress /go to start your adventure.\nPress /help for more information.")


    def handle_go_callback(self, call):
        chat_id = call.message.chat.id # Для простоты предполагаем, что user_id и chat_id идентичны

        pokebol_count = functions.pokebols_number(chat_id)

        if pokebol_count > 0:
            # Обработка нажатия кнопок "Go", "Keep going", "Skip"
            if call.data in ['go', 'keepgoing', 'skip']:
                found_pokemon.clear()
                try:
                    if call.data in ['keepgoing', 'skip']:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                       # удаляет сообщение в котором было нажато "keepgoing, skip"
                    if call.data in ['skip']:
                        bot.delete_message(call.message.chat.id, call.message.message_id-1)
                except Exception as e:
                    print(f"Ошибка при удалении сообщения: {e}")

                if random.choice([True, False]):
                    
                    self.show_catch_or_skip_buttons(chat_id, pokebol_count)
                else:
                    
                    self.back_to_start(chat_id, call.message.message_id)

            # Обработка нажатия кнопок "Catch", "Retry"
            elif call.data in ['catch', 'retry']:
                if call.data == 'retry':
                    bot.delete_message(call.message.chat.id, call.message.message_id)

                if random.choice([True, False]):
                    
                    self.show_captured_or_retry_buttons(chat_id, call.message.message_id)

                else:
                    
                    self.show_captured_or_not_buttons(chat_id, call.message.message_id)


        else:
            bot.send_message(chat_id, "У вас нет pokebol! Найдите или купите их, чтобы продолжить ловлю покемонов.")
            #на будущее: нужно придумать какое то продолжение для пользователя после этого сообщения




    def show_go_buttons(self, chat_id):
        # Отправка кнопки "Go" для начала поиска покемона
        markup = types.InlineKeyboardMarkup()

        button_go = types.InlineKeyboardButton('Go', callback_data='go')
        markup.add(button_go)

        bot.send_message(chat_id, "Press 'Go' to start searching for a Pokemon:", reply_markup=markup)

    def back_to_start(self, chat_id, message_id):
        # Возвращение к начальному состоянию после неудачной попытки
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('Keep going', callback_data='keepgoing')
        markup.add(button_back)
        bot.send_message(chat_id, 'You did not find anything', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)


    def show_pokedex(self, chat_id):
        self.generator = functions.show_pokedex(chat_id)
        markup = types.InlineKeyboardMarkup()
        next_list = types.InlineKeyboardButton('Next', callback_data='next')
        markup.add(next_list)
        bot.send_message(chat_id, next(self.generator), reply_markup=markup)

    def my_pokemons(self, chat_id):
        pokemons = functions.my_pokemons(chat_id)
        # Проверка на пустую строку 'pokedex' перед отправкой
        if pokemons.strip() == '':
            bot.send_message(chat_id, "No Pokemons have been captured yet.")
        else:
            bot.send_message(chat_id, pokemons)



    def show_catch_or_skip_buttons(self, chat_id, pokebol_count):
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
            sent_message = bot.send_document(chat_id, pokemon_photo)
            gen_info = functions.generations[chosen_pokemon]
            if gen_info != '': gen_info = f' ({gen_info})'
            bot.send_message(chat_id, f"You found a {chosen_pokemon}{gen_info}!\n\n It has '{gen}' rarity.\n\n What would you like to do?\n\nYou have {pokebol_count} pokebols",  reply_markup=markup)
            self.states[chat_id] = {'state': 'choose_catch_or_skip', 'message_id': sent_message.message_id, 'gen': gen}
            
            



    def show_captured_or_retry_buttons(self, chat_id, message_id):
        # Отображение кнопки "Keep going" после успешного захвата
        gen = self.states[chat_id].get('gen', '')
        markup = types.InlineKeyboardMarkup()
        button_go = types.InlineKeyboardButton('Keep going', callback_data='go')
        markup.add(button_go)
        functions.capture_pokemon(chat_id, f"{found_pokemon[0]}")
        functions.capture_pokemon_by_rarity(chat_id, f"{found_pokemon[0]}", gen)
        
        bot.send_message(chat_id, f"You captured a {found_pokemon[0]}!", reply_markup=markup)

        #bot.delete_message(chat_id, message_id)

    def show_captured_or_not_buttons(self, chat_id, message_id):
        # Отображение кнопки "Try again" после неудачной попытки захвата
        markup = types.InlineKeyboardMarkup()
        button_try_again = types.InlineKeyboardButton('Try again', callback_data='retry')
        markup.add(button_try_again)
        functions.capture_failed(chat_id)
        bot.send_message(chat_id, 'Bad luck', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)

    def get_pokebols(self, user_id):
        with DatabaseConnection('pokedex.sql') as cur:
            can_get_pokebols = functions.check_pokebols_elegibility(user_id) #возвращает True or False
            text = functions.time_until_next_midnight()
            if can_get_pokebols:
                functions.add_pokebols(user_id, 50, cur)
                bot.send_message(user_id, f'Вы получили 50 бесплатных покеболов. До следующего бесплатного получения осталось {text}')
            else:
                bot.send_message(user_id, f'К сожалению вы еще не можете получить бесплатные покеболы. Дождитесь следующего дня. Осталось ждать: {text}')
        
    def run(self):
        # Запуск бота в режиме бесконечного опроса
        bot.infinity_polling()

# Если файл запущен напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    # Создание экземпляра класса PokemonBot
    pokemon_bot = PokemonBot()

    # Обработчики сообщений и колбеков
    @bot.message_handler(commands=['start'])
    def start_wrapper(message):
        pokemon_bot.start(message)

    @bot.message_handler(commands=['pokedex'])
    def deploy_pokedex(message):
        chat_id = message.chat.id
        pokemon_bot.show_pokedex(chat_id)

    @bot.message_handler(commands=['go'])
    def show_go_message(message):
        chat_id = message.chat.id
        pokemon_bot.show_go_buttons(chat_id)

    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.send_message(message.chat.id, helpinfo, parse_mode='html')

    @bot.message_handler(commands=['get_pokebols'])
    def get_pokebols(message):
        pokemon_bot.get_pokebols(message.chat.id)

    @bot.message_handler(commands=['my_pokemons'])
    def get_pokebols(message):
        pokemon_bot.my_pokemons(message.chat.id)
    
    @bot.message_handler(commands=['rarity'])
    def rarity_command(message):
        bot.send_message(message.chat.id, rarity, parse_mode='html')

    @bot.callback_query_handler(func=lambda call: call.data == "next")
    def scroll_to_next(call):
        markup = types.InlineKeyboardMarkup()
        next_list = types.InlineKeyboardButton('Next', callback_data='next')
        markup.add(next_list)
        try:
            bot.edit_message_text(next(pokemon_bot.generator), call.message.chat.id, call.message.message_id, reply_markup=markup)
        except TypeError:
            bot.edit_message_text('This Pokedex is not valid anymore, press /pokedex to get up-to-date version', call.message.chat.id, call.message.message_id)

    @bot.callback_query_handler(func=lambda call: call.data in ['go', 'keepgoing', 'skip', 'retry', 'catch'])
    def handle_go_callback_wrapper(call):
        markup = types.InlineKeyboardMarkup()
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        pokemon_bot.handle_go_callback(call)


    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler_wrapper(call):
        markup = types.InlineKeyboardMarkup()
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        pokemon_bot.callback_handler(call)

    # Запуск бота
    pokemon_bot.run()