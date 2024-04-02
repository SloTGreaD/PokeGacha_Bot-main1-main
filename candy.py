import asyncio

from functions import AsyncDatabaseConnection

DATABASE_FILE = "pokedex.sql"

async def check_candy_availability(user_id):  
    async with AsyncDatabaseConnection(DATABASE_FILE) as cursor:
        await cursor.execute("SELECT bread FROM items WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
        
async def use_candy(user_id):
    async with AsyncDatabaseConnection(DATABASE_FILE) as cur:
        update_query = 'UPDATE items SET candy = candy - 1 WHERE user_id = ? AND candy > 0'
        await cur.execute(update_query, (user_id,))