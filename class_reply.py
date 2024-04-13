from aiogram import types
import functions
import energy
import info
from info import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





class under_keyboard:
    def __init__(self):
        pass

        
    def reply_menu(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        button2 = KeyboardButton('/🎒My_pokemons')
        button1 = KeyboardButton('/📱Pokedex')
        markup.row(button2, button1)  # Добавление кнопок в один ряд
    
        # Добавление кнопок в другой ряд
        button4 = KeyboardButton('/🍽️Meal')
        button3 = KeyboardButton('/🔴⚪Get_Pokebolls')
        markup.row(button4, button3)  # Добавление кнопок в один ряд
        button5 = KeyboardButton('/🔚End_Adventure')
        markup.add(button5) 
        return markup 
    
    async def back_to_menu(self):

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        # Добавление каждой кнопки в отдельный ряд
        button = KeyboardButton('/🏃‍♂️Start_Adventure')
        button1 = KeyboardButton('/📱Pokedex')
        markup.row(button, button1)  # Добавление кнопок в один ряд
    
        # Добавление кнопок в другой ряд
        button2 = KeyboardButton('/🎒My_pokemons')
        button3 = KeyboardButton('/🔴⚪Get_Pokebolls')
        markup.row(button2, button3)  # Добавление кнопок в один ряд

        # Если хотите добавить одну кнопку в ряд, просто используйте add
        button4 = KeyboardButton('/🍽️Meal')
        button5 = KeyboardButton('/📋Profile')
        markup.add(button4, button5)  # Добавит кнопку в новый ряд
        return markup
    
    async def profile_menu(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton('/📝Change_Nickname')
        button1 = KeyboardButton('/🏠Main_Menu')
        markup.add(button, button1)
        return markup
    
    async def cancel_change_nickname(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton('/❌Discard_Changes')
        markup.add(button)
        return markup

        
