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


