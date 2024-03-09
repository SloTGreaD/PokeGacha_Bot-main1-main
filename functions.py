import random
import sqlite3
import time
import asyncio
import aiosqlite

from datetime import datetime, timedelta
misha_bot_api = '5629818025:AAE3CAZFs6uhMcWZodFUdpKhSJu5awmGK_o'
poke_bot_api = "6831587612:AAEUQ4m30-Pajetdnw0AwZ4omaNmzVkc-4o"

pokemon_list = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'NidoranF', 'Nidorina', 'Nidoqueen', 'NidoranM', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetchd', 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr_Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew']
rarity = {
    "Common": ['Bellsprout', 'Caterpie', 'Diglett', 'Ekans', 'Exeggcute', 'Gastly', 'Goldeen', 'Horsea', 'Krabby', 'Magikarp', 'NidoranF', 'NidoranM', 'Oddish', 'Omanyte', 'Paras', 'Pidgey', 'Poliwag', 'Rattata', 'Shellder', 'Spearow', 'Weedle', 'Zubat'],
    "Uncommon": ['Abra', 'Clefairy', 'Dewgong', 'Doduo', 'Drowzee', 'Dugtrio', 'Geodude', 'Grimer', 'Growlithe', 'Kakuna', 'Koffing', 'Machop', 'Magnemite', 'Mankey', 'Meowth', 'Metapod', 'Pidgeotto', 'Psyduck', 'Sandshrew', 'Seel', 'Staryu', 'Tentacool', 'Venonat', 'Voltorb', 'Weepinbell'],
    "Rare": ['Beedrill', 'Bulbasaur', 'Chansey', 'Charmander', 'Cubone', 'Eevee', 'Electrode', 'Fearow', 'Gloom', 'Golbat', 'Graveler', 'Haunter', 'Jigglypuff', 'Jynx', 'Kadabra', 'Kingler', 'Nidorina', 'Nidorino', 'Omastar', 'Parasect', 'Persian', 'Pikachu', 'Pinsir', 'Poliwhirl', 'Ponyta', 'Raticate', 'Rhyhorn', 'Seaking', 'Slowpoke', 'Squirtle', 'Tangela', 'Venomoth', 'Vulpix'],
    "SuperRare": ['Arbok', 'Butterfree', 'Charmeleon', 'Clefable', 'Cloyster', 'Dodrio', 'Dratini', 'Electabuzz', 'Exeggutor', 'Golduck', 'Hitmonchan', 'Hitmonlee', 'Hypno', 'Ivysaur', 'Kabuto', 'Kangaskhan', 'Lapras', 'Lickitung', 'Machoke', 'Magmar', 'Magneton', 'Mr_Mime', 'Onix', 'Pidgeot', 'Poliwrath', 'Porygon', 'Primeape', 'Rapidash', 'Sandslash', 'Scyther', 'Seadra', 'Slowbro', 'Starmie', 'Tauros', 'Tentacruel', 'Victreebel', 'Vileplume', 'Wartortle', 'Weezing', 'Wigglytuff'],
    "Epic": ['Aerodactyl', 'Alakazam', 'Arcanine', 'Blastoise', 'Charizard', 'Dragonair', 'Farfetchd', 'Flareon', 'Gengar', 'Golem', 'Gyarados', 'Jolteon', 'Kabutops', 'Machamp', 'Marowak', 'Muk', 'Nidoking', 'Nidoqueen', 'Ninetales', 'Raichu', 'Rhydon', 'Snorlax', 'Vaporeon', 'Venusaur'],
    "Legendary": ['Zapdos', 'Moltres', 'Mewtwo', 'Mew', 'Dragonite', 'Ditto', 'Articuno']
}

generations = {'Bellsprout': '', 'Caterpie': '', 'Diglett': '', 'Ekans': '', 'Exeggcute': '', 'Gastly': '', 'Goldeen': '', 'Horsea': '', 'Krabby': '', 'Magikarp': '', 'NidoranF': '', 'NidoranM': '', 'Oddish': '', 'Omanyte': '', 'Paras': '', 'Pidgey': '', 'Poliwag': '', 'Rattata': '', 'Shellder': '', 'Spearow': '', 'Weedle': '', 'Zubat': '', 'Abra': '', 'Clefairy': '', 'Dewgong': "Seel's evolution", 'Doduo': '', 'Drowzee': '', 'Dugtrio': "Diglett's evolution", 'Geodude': '', 'Grimer': '', 'Growlithe': '', 'Kakuna': "Weedle's 1'st evolution", 'Koffing': '', 'Machop': '', 'Magnemite': '', 'Mankey': '', 'Meowth': '', 'Metapod': "Caterpie's 1'st evolution", 'Pidgeotto': "Pidgey's 1'st evolution", 'Psyduck': '', 'Sandshrew': '', 'Seel': '', 'Staryu': '', 'Tentacool': '', 'Venonat': '', 'Voltorb': '', 'Weepinbell': "Bellsprout's 1'st evolution", 'Beedrill': "Weedle's 2'nd evolution", 'Bulbasaur': '', 'Chansey': '', 'Charmander': '', 'Cubone': '', 'Eevee': '', 'Electrode': "Voltorb's evolution", 'Fearow': "Spearow's evolution", 'Gloom': "Oddish's 1'st evolution", 'Golbat': "Zubat's evolution", 'Graveler': "Geodude's 1'st evolution", 'Haunter': "Gastly's 1'st evolution", 'Jigglypuff': '', 'Jynx': '', 'Kadabra': "Abra's 1'st evolution", 'Kingler': "Krabby's evolution", 'Nidorina': "NidoranF's 1'st evolution", 'Nidorino': "NidoranM's evolution", 'Omastar': "Omanyte's evolution", 'Parasect': "Paras's evolution", 'Persian': "Meowth's evolution", 'Pikachu': '', 'Pinsir': '', 'Poliwhirl': "Poliwag's 1'st evolution", 'Ponyta': '', 'Raticate': "Rattata's evolution", 'Rhyhorn': '', 'Seaking': "Goldeen's evolution", 'Slowpoke': '', 'Squirtle': '', 'Tangela': '', 'Venomoth': "Venonat's evolution", 'Vulpix': '', 'Arbok': "Ekan's evolution", 'Butterfree': "Caterpie's 2'nd evolution", 'Charmeleon': "Charmander's 1'st evolution", 'Clefable': "Clefairy's evolution", 'Cloyster': "Shellder's evolution", 'Dodrio': "Doduo's evolution", 'Dratini': '', 'Electabuzz': '', 'Exeggutor': "Exeggcute's evolution", 'Golduck': "Psyduck's evolution", 'Hitmonchan': '', 'Hitmonlee': '', 'Hypno': "Drowzee's evolution", 'Ivysaur': "Bulbasaur's 1'st evolution", 'Kabuto': '', 'Kangaskhan': '', 'Lapras': '', 'Lickitung': '', 'Machoke': "Machop's 1'st evolution", 'Magmar': '', 'Magneton': "Magnemite's evolution", 'Mr_Mime': '', 'Onix': '', 'Pidgeot': "Pidgey's 2'st evolution", 'Poliwrath': "Poliwag's 2'nd evolution", 'Porygon': '', 'Primeape': "Mankey's evolution", 'Rapidash': "Ponyta's evolution", 'Sandslash': "Sandshrew's evolution", 'Scyther': '', 'Seadra': "Horsea's evolution", 'Slowbro': "Slowpoke's evolution", 'Starmie': "Staryu's evolution", 'Tauros': '', 'Tentacruel': "Tentacool's evolution", 'Victreebel': "Bellsprout's 2'nd evolution", 'Vileplume': "Oddish's 2'nd evolution", 'Wartortle': "Squirtle's 1'st evolution", 'Weezing': "Koffing's evolution", 'Wigglytuff': "Jigglypuff's evolution", 'Aerodactyl': '', 'Alakazam': "Abra's 2'nd evolution", 'Arcanine': "Growlithe's evolution", 'Blastoise': "Squirtle's 2'nd evolution", 'Charizard': "Charmander's 2'nd evolution", 'Dragonair': "Dratini's 1'st evolution", 'Farfetchd': '', 'Flareon': "Eevee's evolution", 'Gengar': "Gastly's 2'nd evolution", 'Golem': "Geodude's 2'nd evolution", 'Gyarados': "Magikarp's evolution", 'Jolteon': "Eevee's evolution", 'Kabutops': "Kabuto's evolution", 'Machamp': "Machop's 2'nd evolution", 'Marowak': "Cubone's evolution", 'Muk': "Grimer's evolution", 'Nidoking': "NidoranM's evolution", 'Nidoqueen': "Nidorina's evolution", 'Ninetales': "Vulpix's evolution", 'Raichu': "Pikachu's evolution", 'Rhydon': "Rhyhorn's evolution", 'Snorlax': '', 'Vaporeon': "Eevee's evolution", 'Venusaur': "Bulbasaur's 2'nd evolution", 'Zapdos': '', 'Moltres': '', 'Mewtwo': '', 'Mew': '', 'Dragonite': "Dratini's 2'nd evolution", 'Ditto': '', 'Articuno': ''}

def pokemon_catch():  # возвращает рандомное имя покемона в зависимости от их вероятности выпадения
    dictio = {"Common":'600',
              "Uncommon":'230',
              "Rare":'120',       # key - веротность выпаения покемона, value -  list с именами покемонов
              "SuperRare":'30',
              "Epic":'19',   # вероятности должны быть написаны целыми числами
              "Legendary":'1'}



    rand_num = random.randint(1, 1000) # вероятности должны в сумме давать 1000
    counter = 0
    for key in dictio:
        counter += int(dictio[key])
        if counter >= rand_num:
            pokemon_name = random.choice(rarity[key])
            return pokemon_name, key
        

class AsyncDatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_name)
        return await self.conn.cursor()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.commit()
        await self.conn.close()




async def create_all_tables():
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        text = "CREATE TABLE IF NOT EXISTS number_of_pokemons (user_id INTEGER, last_access_date VARCHAR(12) DEFAULT '10/12/15', pokebols INTEGER DEFAULT 5, "
        text += "".join(f'{item.lower()} INTEGER DEFAULT 0,' for item in pokemon_list)
        text = text.rstrip(',') + ")"
        await cur.execute(text)
        await cur.execute('''
            CREATE TABLE IF NOT EXISTS captured_pokemons (
            user_id INTEGER,
            found_pokemon VARCHAR(20),
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        await cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50))')
        await cur.execute('''CREATE TABLE IF NOT EXISTS dif_rarity 
                    (user_id INTEGER,
                     legendary VARCHAR(30),
                     epic VARCHAR(30),
                    superrare VARCHAR(30),
                     rare VARCHAR(30),
                     uncommon VARCHAR(30),
                     common VARCHAR(30)
                    )''')

async def add_user_to_number_of_pokemons(user_id):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        check_query = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(check_query, (user_id,))
        result = await cur.fetchone()
        if result is None:
            insert_query = "INSERT INTO number_of_pokemons (user_id) VALUES (?)"
            await cur.execute(insert_query, (user_id,))

    

async def capture_pokemon(user_id, found_pokemon):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        num = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(num, (user_id,))
        pokebol_count = (await cur.fetchone())[0]

        if pokebol_count > 0:
            found_pokemon = found_pokemon.lower()
            cap = "INSERT INTO captured_pokemons (user_id, found_pokemon) VALUES (?, ?)"
            await cur.execute(cap, (user_id, found_pokemon))
            query = f"UPDATE number_of_pokemons SET {found_pokemon} = {found_pokemon} + 1, pokebols = pokebols - 1 WHERE user_id = ?"
            await cur.execute(query, (user_id,))
            success = True
        else:
            success = False
    return success
async def capture_pokemon_by_rarity(user_id, found_pokemon, gen):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        # Проверяем количество pokebols у пользователя
        num = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(num, (user_id,))
        pokebol_count = await cur.fetchone()

        if pokebol_count and pokebol_count[0] > 0:
            found_pokemon = found_pokemon.lower()
            # Выполняем логику захвата в зависимости от редкости
            capture_query = None
            if gen == 'Common':
                capture_query = "INSERT INTO dif_rarity (user_id, common) VALUES (?, ?)"
            elif gen == 'Uncommon':
                capture_query = "INSERT INTO dif_rarity (user_id, uncommon) VALUES (?, ?)"
            elif gen == 'Rare':
                capture_query = "INSERT INTO dif_rarity (user_id, rare) VALUES (?, ?)"
            elif gen == 'SuperRare':
                capture_query = "INSERT INTO dif_rarity (user_id, superrare) VALUES (?, ?)"
            elif gen == 'Epic':
                capture_query = "INSERT INTO dif_rarity (user_id, epic) VALUES (?, ?)"
            elif gen == 'Legendary':
                capture_query = "INSERT INTO dif_rarity (user_id, legendary) VALUES (?, ?)"

            if capture_query:
                await cur.execute(capture_query, (user_id, found_pokemon))
                await cur.execute("UPDATE number_of_pokemons SET pokebols = pokebols - 1 WHERE user_id = ?", (user_id,))
                success = True
            else:
                success = False
        else:
            success = False

    return success

async def capture_failed (user_id):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        pok = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(pok, (user_id,))
        pokebol_count = await cur.fetchone()[0]

        if pokebol_count > 0:
            num2 = "UPDATE number_of_pokemons SET pokebols = pokebols - 1 WHERE user_id = ?"
            await cur.execute(num2, (user_id,))
        

async def show_capture_time(user_id): #показывает время когда словил каждого покемона
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        cap1 = 'SELECT * FROM captured_pokemons WHERE user_id = ?'
        await cur.execute(cap1, (user_id,))
        info = await cur.fetchall()
        pokedex = ''
        for el in info:
            # Убедитесь, что здесь правильно форматируете строку, например:
            pokedex += f"Pokemon: {el[1]}, Captured At: {el[2]}\n"
    
    return pokedex


async def show_pokedex(user_id):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        num3 = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(num3, (user_id,))
        #собирает всю информацию о покемонах и конкатенирует все в лист_lines_list
        pokemon_amount = await cur.fetchone()[3:]
        pokemons = ("".join(f'{pokemon} {"🟢" if amount>0 else "🔴"}') for pokemon, amount in zip(pokemon_list, pokemon_amount))
        lines = (f"{num}. {pokemon}" for num, pokemon in enumerate(pokemons, 1))
        lines_list = list(lines)
        while True:
            #разбивает лист на равные куски по 25 покемонов, (последний кусок 26) и возвращает ганератор с нужным текстом
            for chunk_start in range(0, 150, 25):
                if chunk_start == 125:
                    yield '\n'.join(lines_list[chunk_start : chunk_start + 26])
                else:
                    yield '\n'.join(lines_list[chunk_start : chunk_start + 25])


async def my_pokemons(user_id):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        num4 = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(num4, (user_id,))
        pokemons = await cur.fetchone()

        if pokemons is None:
            return "You haven't caught any Pokémon yet."
        
        text = f'You have:\nPokebols: {pokemons[2]}'
        # for poke_count, pokemon_name in zip(pokemons[3:], pokemon_list):
        #     if poke_count > 0:
        #         text += f'{pokemon_name}: {poke_count}\n'
        text = '\n'.join((text,"\n".join(f'{pokemon_name}: {poke_count}' for poke_count, pokemon_name in zip(pokemons[3:], pokemon_list) if poke_count > 0)))
        #     text = f"""You have:
        # Pokebols: {pokemons[2]}
        # Pikachu: {pokemons[3]}
        # Squirtle: {pokemons[4]}
        # Bulbasaur: {pokemons[5]}
        # Charmander: {pokemons[6]}
        # """
    
    return text

async def add_pokebols(user_id, amount, cur):
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        update_query = "UPDATE number_of_pokemons SET pokebols = pokebols + ? WHERE user_id = ?"
        await cur.execute(update_query, (amount, user_id))

async def pokebols_number(user_id):
    number = 0
    async with AsyncDatabaseConnection('pokedex.sql') as cur:
        num5 = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        await cur.execute(num5, (user_id,))
        result = await cur.fetchone()
        if result:
            number = int(result[0])
    return number



#проверяет последнюю дату запроса юзера на получение покеболов, и если это новый день, дает разрешение и перезаписывает дату
async def check_pokebols_elegibility(user_id):
    async with AsyncDatabaseConnection('pokedex.sql') as cursor:  # cursor уже является курсором
        await cursor.execute('SELECT last_access_date FROM number_of_pokemons WHERE user_id = ?', (user_id,))
        date_result = await cursor.fetchone()
        if date_result:
            date = date_result[0]
            now = datetime.now()
            current_date = now.strftime("%d/%m/%y")
            if date != current_date:
                await cursor.execute("UPDATE number_of_pokemons SET last_access_date = ? WHERE user_id = ?", (current_date, user_id))
                return True
            else:
                return False
        else:
            return False
        
def time_until_next_midnight():
    current_time = datetime.now()
    next_midnight = datetime(current_time.year, current_time.month, current_time.day) + timedelta(days=1)
    time_remaining = next_midnight - current_time
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes = remainder // 60
    return f'{hours} часов, {minutes+1} минут'





if __name__ == "__main__":

    # print(show_pokedex(668210174))
    # print(time_until_next_midnight())
    a = show_pokedex(668210174)
    print(a.__next__())










