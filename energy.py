
import asyncio

from datetime import datetime, timedelta
from functions import AsyncDatabaseConnection
from info import POKEMON_LIST, RARITY_DICT, GenerationProbabilities


DATABASE_FILE = "pokedex.sql"




async def check_bread_availability(user_id):  # проверяет наличие хлеба
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute("SELECT bread FROM items WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
        
async def check_rice_availability(user_id):  # проверяет наличие хлеба
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute("SELECT rice FROM items WHERE user_id = ?", (user_id,))
        result1 = await cursor.fetchone()
        if result1 and result1[0] > 0:
            return True
        else:
            return False

async def check_ramen_availability(user_id):  # проверяет наличие хлеба
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute("SELECT ramen FROM items WHERE user_id = ?", (user_id,))
        result2 = await cursor.fetchone()
        if result2 and result2[0] > 0:
            return True
        else:
            return False
        
async def check_spaghetti_availability(user_id):  # проверяет наличие хлеба
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute("SELECT spaghetti FROM items WHERE user_id = ?", (user_id,))
        result2 = await cursor.fetchone()
        if result2 and result2[0] > 0:
            return True
        else:
            return False


        
async def use_energy(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query = 'UPDATE items SET energy = energy - 1 WHERE user_id = ? AND energy > 0'
        await cur.execute(update_query, (user_id,))


async def use_bread(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query1 = 'UPDATE items SET energy = energy + 10 WHERE user_id = ?'
        update_query2 = 'UPDATE items SET bread = bread - 1 WHERE user_id = ? AND bread > 0'
        await cur.execute(update_query1, (user_id,))
        await cur.execute(update_query2, (user_id,))

async def use_rice(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query1 = 'UPDATE items SET energy = energy + 15 WHERE user_id = ?'
        update_query2 = 'UPDATE items SET rice = rice - 1 WHERE user_id = ? AND rice > 0'
        await cur.execute(update_query1, (user_id,))
        await cur.execute(update_query2, (user_id,))

async def use_ramen(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query1 = 'UPDATE items SET energy = energy + 25 WHERE user_id = ?'
        update_query2 = 'UPDATE items SET ramen = ramen - 1 WHERE user_id = ? AND ramen > 0'
        await cur.execute(update_query1, (user_id,))
        await cur.execute(update_query2, (user_id,))

async def use_spaghetti(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query1 = 'UPDATE items SET energy = energy + 40 WHERE user_id = ?'
        update_query2 = 'UPDATE items SET spaghetti = spaghetti - 1 WHERE user_id = ? AND spaghetti > 0'
        await cur.execute(update_query1, (user_id,))
        await cur.execute(update_query2, (user_id,))


async def add_energy(user_id, amount1):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query1 = "UPDATE items SET energy = energy + ? WHERE user_id = ?"
        await cur.execute(update_query1, (amount1, user_id))


async def check_last_adventure(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute('SELECT last_adventure_date FROM items WHERE user_id = ?', (user_id,))
        date_result2 = await cursor.fetchone()
        if date_result2:
            date = date_result2[0]
            now = datetime.now()
            current_date2 = now.strftime("%d/%m/%y")
            if date != current_date2:
                await cursor.execute("UPDATE items SET last_adventure_date = ? WHERE user_id = ?",
                                     (current_date2, user_id))
                return True
            else:
                return False
        else:
            return False
        
async def check_energy_eligibility(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute('SELECT last_rest_date FROM items WHERE user_id = ?', (user_id,))
        date_result1 = await cursor.fetchone()
        if date_result1:
            date = date_result1[0]
            now = datetime.now()
            current_date1 = now.strftime("%d/%m/%y")
            if date != current_date1:
                await cursor.execute("UPDATE items SET last_rest_date = ? WHERE user_id = ?",
                                     (current_date1, user_id))
                return True
            else:
                return False
        else:
            return False
        
async def energy_number(user_id):
    count = 0
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        query1 = 'SELECT energy FROM items WHERE user_id = ?'
        await cur.execute(query1, (user_id,))
        result = await cur.fetchone()
        if result:
            count = int(result[0])
    return count


async def main():
    await add_energy(668210174, 100)

if __name__ == "__main__":
    asyncio.run(main())
