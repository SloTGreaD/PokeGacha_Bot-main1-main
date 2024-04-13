from aiogram import types
from info import bot, dp
import aiosqlite
from functions import AsyncDatabaseConnection

DATABASE_FILE = "pokedex.sql"


    

async def check_user_nickname(user_id):
    """
    Проверяет, есть ли у user_id nikname.
    Возвращает True, если nikname есть, иначе False.
    """
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        cursor = await cur.execute("SELECT nickname FROM number_of_pokemons WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        return result is not None and result[0] is not None

async def register_new_user(user_id, nickname):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        # Предполагаемый правильный запрос:
        await cur.execute("INSERT INTO number_of_pokemons (user_id, nickname) VALUES (?, ?)", (user_id, nickname))
        await cur.execute("INSERT INTO captured_pokemons (user_id, nickname) VALUES (?, ?)", (user_id, nickname))
        await cur.execute("INSERT INTO items (user_id, nickname) VALUES (?, ?)", (user_id, nickname))
    
async def is_nickname_taken(nickname):
    """
    Проверяет, занят ли никнейм.
    Возвращает True, если никнейм уже используется кем-то, иначе False.
    """
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        cursor = await cur.execute("SELECT user_id FROM number_of_pokemons WHERE nickname = ?", (nickname,))
        result = await cursor.fetchone()
        return result is not None
    
async def get_user_profile(user_id):
    """ Получает профиль пользователя из базы данных. """
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        cursor = await cur.execute("SELECT nickname FROM number_of_pokemons WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else 'Unknown'

async def update_nickname(user_id, new_nickname):
    """
    Обновляет никнейм пользователя с заданным user_id.
    """
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        await cur.execute("UPDATE number_of_pokemons SET nickname = ? WHERE user_id = ?", (new_nickname, user_id))
        
