import random
import sqlite3
import time
from info import helpinfo

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
        

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def create_users_table():
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50))')
    conn.commit()
    conn.close()



def create_captured_pokemons_table():
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS captured_pokemons (
        user_id INTEGER,
        found_pokemon VARCHAR(20),
        captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    conn.commit()
    conn.close()

def create_number_of_pokemons(): #таблица для учета количества покемонов у каждого юзера
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()

    text = "CREATE TABLE IF NOT EXISTS number_of_pokemons (user_id INTEGER, last_access_date VARCHAR(12) DEFAULT '10/12/15', pokebols INTEGER DEFAULT 5, "
    # for item in pokemon_list:     #создаем таблицу с покемонами из этого листа, который был идентифицирован ранее
    #     text += f'{item.lower()} INTEGER DEFAULT 0,'
    text += "".join(f'{item.lower()} INTEGER DEFAULT 0,' for item in pokemon_list)
    text = text.rstrip(',') + ")"
    cur.execute(text)
    conn.commit()
    conn.close()

def create_all_tables():
    with DatabaseConnection('pokedex.sql') as cur:
        text = "CREATE TABLE IF NOT EXISTS number_of_pokemons (user_id INTEGER, last_access_date VARCHAR(12) DEFAULT '10/12/15', pokebols INTEGER DEFAULT 5,  "
        # for item in pokemon_list:     #создаем таблицу с покемонами из этого листа, который был идентифицирован ранее
        #     text += f'{item.lower()} INTEGER DEFAULT 0,'
        text += "".join(f'{item.lower()} INTEGER DEFAULT 0,' for item in pokemon_list)
        text = text.rstrip(',') + ")"
        cur.execute(text)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS captured_pokemons (
            user_id INTEGER,
            found_pokemon VARCHAR(20),
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50))')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS dif_rarity 
                    (user_id INTEGER,
                     legendary VARCHAR(30),
                     epic VARCHAR(30),
                    superrare VARCHAR(30),
                     rare VARCHAR(30),
                     uncommon VARCHAR(30),
                     common VARCHAR(30)
                    )''')

def add_user_to_number_of_pokemons(user_id):
    with DatabaseConnection('pokedex.sql') as cur:
        check_query = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(check_query, (user_id,))
        result = cur.fetchone()  # Получаем результат выполнения запроса
        if result is None:  # Проверяем, существует ли уже пользователь
            insert_query = "INSERT INTO number_of_pokemons (user_id) VALUES (?)"
            cur.execute(insert_query, (user_id,))

    

def capture_pokemon(user_id, found_pokemon): #добавляет название покемона в таблицу с временами когда словил покемона и таблицу с количеством словленных покемонов
    with DatabaseConnection('pokedex.sql') as cur:
        # Проверяем количество pokebols у пользователя
        num = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(num, (user_id,))
        pokebol_count = cur.fetchone()[0]

        if pokebol_count > 0:
            found_pokemon = found_pokemon.lower()
            # Выполняем логику захвата

            cap = "INSERT INTO captured_pokemons (user_id, found_pokemon) VALUES (?, ?)"
            cur.execute(cap, (user_id, found_pokemon))
            query = f"UPDATE number_of_pokemons SET {found_pokemon} = {found_pokemon} + 1, pokebols = pokebols - 1 WHERE user_id = ?"
            cur.execute(query, (user_id,))
        
            success = True
        else:
            success = False

    
    return success
def capture_pokemon_by_rarity(user_id, found_pokemon, gen):
    with DatabaseConnection('pokedex.sql') as cur:
        # Проверяем количество pokebols у пользователя
        num = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(num, (user_id,))
        pokebol_count = cur.fetchone()[0]

        if pokebol_count > 0:
            found_pokemon = found_pokemon.lower()
            # Выполняем логику захвата
            if gen == 'Common':
                cap0 = "INSERT INTO dif_rarity (user_id, common) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon))
            elif gen == 'Uncommon':
                cap0 = "INSERT INTO dif_rarity (user_id, uncommon) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon))   
            elif gen == 'Rare':
                cap0 = "INSERT INTO dif_rarity (user_id, rare) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon))
            elif gen == 'SuperRare':
                cap0 = "INSERT INTO dif_rarity (user_id, superrare) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon)) 
            elif gen == 'Epic':
                cap0 = "INSERT INTO dif_rarity (user_id, epic) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon))       
            elif gen == 'Legendary':
                cap0 = "INSERT INTO dif_rarity (user_id, legendary) VALUES (?, ?)"
                cur.execute(cap0, (user_id, found_pokemon))
                
            success = True
        else:
            success = False

    return success

def capture_failed (user_id):
    with DatabaseConnection('pokedex.sql') as cur:
        pok = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(pok, (user_id,))
        pokebol_count = cur.fetchone()[0]

        if pokebol_count > 0:
            num2 = "UPDATE number_of_pokemons SET pokebols = pokebols - 1 WHERE user_id = ?"
            cur.execute(num2, (user_id,))
        

def show_capture_time(user_id): #показывает время когда словил каждого покемона
    with DatabaseConnection('pokedex.sql') as cur:
        cap1 = 'SELECT * FROM captured_pokemons WHERE user_id = ?'
        cur.execute(cap1, (user_id,))
        info = cur.fetchall()
        pokedex = ''
        for el in info:
            # Убедитесь, что здесь правильно форматируете строку, например:
            pokedex += f"Pokemon: {el[1]}, Captured At: {el[2]}\n"
    
    return pokedex


def show_pokedex(user_id):
    with DatabaseConnection('pokedex.sql') as cur:
        num3 = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(num3, (user_id,))
        #собирает всю информацию о покемонах и конкатенирует все в лист_lines_list
        pokemon_amount = cur.fetchone()[3:]
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


def my_pokemons(user_id):
    with DatabaseConnection('pokedex.sql') as cur:
        num4 = 'SELECT * FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(num4, (user_id,))
        pokemons = cur.fetchone()

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

def add_pokebols(user_id, amount, cur):
    with DatabaseConnection('pokedex.sql') as cur:
        update_query = "UPDATE number_of_pokemons SET pokebols = pokebols + ? WHERE user_id = ?"
        cur.execute(update_query, (amount, user_id))

def pokebols_number(user_id):
    number = 0
    with DatabaseConnection('pokedex.sql') as cur:
        num5 = 'SELECT pokebols FROM number_of_pokemons WHERE user_id = ?'
        cur.execute(num5, (user_id,))
        result = cur.fetchone()
        if result:
            number = int(result[0])
    return number



#проверяет последнюю дату запроса юзера на получение покеболов, и если это новый день, дает разрешение и перезаписывает дату
def check_pokebols_elegibility(user_id):
    can_get_pokemons = False
    with DatabaseConnection('pokedex.sql') as cursor:
        num6 = 'SELECT last_access_date from number_of_pokemons where user_id = ?'
        cursor.execute(num6, (user_id,))
        date = cursor.fetchone()[0]
        now = datetime.now()
        current_date = now.strftime("%d/%m/%y")
        if date != current_date:
            can_get_pokemons = True
            num7 = "UPDATE number_of_pokemons SET last_access_date = ? WHERE user_id = ?"
            cursor.execute(num7, (current_date, user_id))
    return can_get_pokemons

def time_until_next_midnight():
    current_time = datetime.now()
    next_midnight = datetime(current_time.year, current_time.month, current_time.day) + timedelta(days=1)
    time_remaining = next_midnight - current_time
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes = remainder // 60
    return f'{hours} часов, {minutes+1} минут'




if __name__ == "__main__":
    print(helpinfo)










