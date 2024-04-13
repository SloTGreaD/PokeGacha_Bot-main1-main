from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

MISHA_BOT_API = '5629818025:AAE3CAZFs6uhMcWZodFUdpKhSJu5awmGK_o'
POKE_BOT_API = "6831587612:AAEUQ4m30-Pajetdnw0AwZ4omaNmzVkc-4o"

TOKEN = POKE_BOT_API
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

HelpInfo = """
<b>Помощь по использованию бота:</b>

/start - Начать поиск покемона
/go - идти
/help - Вывести это сообщение справки
/pokedex - Показать Покемонов
/get_pokebols - получить 5 бесплатных покемонов за ежедневный вход 
/my_pokemons - посмотреть всех своих покемонов
/rarity - все редкости и шанс выпадения
/have_a_rest - отдохнуть
<b>Дополнительные команды:</b>

/help - Вывести это сообщение справки

<b>Обратите внимание:</b>
- После каждой успешной или неудачной попытки поиска вам будут предоставлены соответствующие опции.
<b>go</b> - Попробовать поймать покемона
<b>keepgoing</b> - Продолжить поиски
<b>skip</b> - Пропустить и попробовать еще раз
<b>retry</b> - Повторить попытку
- Удачи в поисках покемонов!
"""

RARITY = 'Common: 60%\nUncommon: 23%\nRare: 12%\nSuperRare: 3%\nEpic: 1.9%\nLegendary: 0.1%'

POKEMON_LIST = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'NidoranF', 'Nidorina', 'Nidoqueen', 'NidoranM', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetchd', 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr_Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew']

RARITY_DICT = {
    "Common": ['Bellsprout', 'Caterpie', 'Diglett', 'Ekans', 'Exeggcute', 'Gastly', 'Goldeen', 'Horsea', 'Krabby', 'Magikarp', 'NidoranF', 'NidoranM', 'Oddish', 'Omanyte', 'Paras', 'Pidgey', 'Poliwag', 'Rattata', 'Shellder', 'Spearow', 'Weedle', 'Zubat'],
    "Uncommon": ['Abra', 'Clefairy', 'Dewgong', 'Doduo', 'Drowzee', 'Dugtrio', 'Geodude', 'Grimer', 'Growlithe', 'Kakuna', 'Koffing', 'Machop', 'Magnemite', 'Mankey', 'Meowth', 'Metapod', 'Pidgeotto', 'Psyduck', 'Sandshrew', 'Seel', 'Staryu', 'Tentacool', 'Venonat', 'Voltorb', 'Weepinbell'],
    "Rare": ['Beedrill', 'Bulbasaur', 'Chansey', 'Charmander', 'Cubone', 'Eevee', 'Electrode', 'Fearow', 'Gloom', 'Golbat', 'Graveler', 'Haunter', 'Jigglypuff', 'Jynx', 'Kadabra', 'Kingler', 'Nidorina', 'Nidorino', 'Omastar', 'Parasect', 'Persian', 'Pikachu', 'Pinsir', 'Poliwhirl', 'Ponyta', 'Raticate', 'Rhyhorn', 'Seaking', 'Slowpoke', 'Squirtle', 'Tangela', 'Venomoth', 'Vulpix'],
    "SuperRare": ['Arbok', 'Butterfree', 'Charmeleon', 'Clefable', 'Cloyster', 'Dodrio', 'Dratini', 'Electabuzz', 'Exeggutor', 'Golduck', 'Hitmonchan', 'Hitmonlee', 'Hypno', 'Ivysaur', 'Kabuto', 'Kangaskhan', 'Lapras', 'Lickitung', 'Machoke', 'Magmar', 'Magneton', 'Mr_Mime', 'Onix', 'Pidgeot', 'Poliwrath', 'Porygon', 'Primeape', 'Rapidash', 'Sandslash', 'Scyther', 'Seadra', 'Slowbro', 'Starmie', 'Tauros', 'Tentacruel', 'Victreebel', 'Vileplume', 'Wartortle', 'Weezing', 'Wigglytuff'],
    "Epic": ['Aerodactyl', 'Alakazam', 'Arcanine', 'Blastoise', 'Charizard', 'Dragonair', 'Farfetchd', 'Flareon', 'Gengar', 'Golem', 'Gyarados', 'Jolteon', 'Kabutops', 'Machamp', 'Marowak', 'Muk', 'Nidoking', 'Nidoqueen', 'Ninetales', 'Raichu', 'Rhydon', 'Snorlax', 'Vaporeon', 'Venusaur'],
    "Legendary": ['Zapdos', 'Moltres', 'Mewtwo', 'Mew', 'Dragonite', 'Ditto', 'Articuno']
}
GENERATIONS = {'Bellsprout': '', 'Caterpie': '', 'Diglett': '', 'Ekans': '', 'Exeggcute': '', 'Gastly': '', 'Goldeen': '', 'Horsea': '', 'Krabby': '', 'Magikarp': '', 'NidoranF': '', 'NidoranM': '', 'Oddish': '', 'Omanyte': '', 'Paras': '', 'Pidgey': '', 'Poliwag': '', 'Rattata': '', 'Shellder': '', 'Spearow': '', 'Weedle': '', 'Zubat': '', 'Abra': '', 'Clefairy': '', 'Dewgong': "Seel's evolution", 'Doduo': '', 'Drowzee': '', 'Dugtrio': "Diglett's evolution", 'Geodude': '', 'Grimer': '', 'Growlithe': '', 'Kakuna': "Weedle's 1'st evolution", 'Koffing': '', 'Machop': '', 'Magnemite': '', 'Mankey': '', 'Meowth': '', 'Metapod': "Caterpie's 1'st evolution", 'Pidgeotto': "Pidgey's 1'st evolution", 'Psyduck': '', 'Sandshrew': '', 'Seel': '', 'Staryu': '', 'Tentacool': '', 'Venonat': '', 'Voltorb': '', 'Weepinbell': "Bellsprout's 1'st evolution", 'Beedrill': "Weedle's 2'nd evolution", 'Bulbasaur': '', 'Chansey': '', 'Charmander': '', 'Cubone': '', 'Eevee': '', 'Electrode': "Voltorb's evolution", 'Fearow': "Spearow's evolution", 'Gloom': "Oddish's 1'st evolution", 'Golbat': "Zubat's evolution", 'Graveler': "Geodude's 1'st evolution", 'Haunter': "Gastly's 1'st evolution", 'Jigglypuff': '', 'Jynx': '', 'Kadabra': "Abra's 1'st evolution", 'Kingler': "Krabby's evolution", 'Nidorina': "NidoranF's 1'st evolution", 'Nidorino': "NidoranM's evolution", 'Omastar': "Omanyte's evolution", 'Parasect': "Paras's evolution", 'Persian': "Meowth's evolution", 'Pikachu': '', 'Pinsir': '', 'Poliwhirl': "Poliwag's 1'st evolution", 'Ponyta': '', 'Raticate': "Rattata's evolution", 'Rhyhorn': '', 'Seaking': "Goldeen's evolution", 'Slowpoke': '', 'Squirtle': '', 'Tangela': '', 'Venomoth': "Venonat's evolution", 'Vulpix': '', 'Arbok': "Ekan's evolution", 'Butterfree': "Caterpie's 2'nd evolution", 'Charmeleon': "Charmander's 1'st evolution", 'Clefable': "Clefairy's evolution", 'Cloyster': "Shellder's evolution", 'Dodrio': "Doduo's evolution", 'Dratini': '', 'Electabuzz': '', 'Exeggutor': "Exeggcute's evolution", 'Golduck': "Psyduck's evolution", 'Hitmonchan': '', 'Hitmonlee': '', 'Hypno': "Drowzee's evolution", 'Ivysaur': "Bulbasaur's 1'st evolution", 'Kabuto': '', 'Kangaskhan': '', 'Lapras': '', 'Lickitung': '', 'Machoke': "Machop's 1'st evolution", 'Magmar': '', 'Magneton': "Magnemite's evolution", 'Mr_Mime': '', 'Onix': '', 'Pidgeot': "Pidgey's 2'st evolution", 'Poliwrath': "Poliwag's 2'nd evolution", 'Porygon': '', 'Primeape': "Mankey's evolution", 'Rapidash': "Ponyta's evolution", 'Sandslash': "Sandshrew's evolution", 'Scyther': '', 'Seadra': "Horsea's evolution", 'Slowbro': "Slowpoke's evolution", 'Starmie': "Staryu's evolution", 'Tauros': '', 'Tentacruel': "Tentacool's evolution", 'Victreebel': "Bellsprout's 2'nd evolution", 'Vileplume': "Oddish's 2'nd evolution", 'Wartortle': "Squirtle's 1'st evolution", 'Weezing': "Koffing's evolution", 'Wigglytuff': "Jigglypuff's evolution", 'Aerodactyl': '', 'Alakazam': "Abra's 2'nd evolution", 'Arcanine': "Growlithe's evolution", 'Blastoise': "Squirtle's 2'nd evolution", 'Charizard': "Charmander's 2'nd evolution", 'Dragonair': "Dratini's 1'st evolution", 'Farfetchd': '', 'Flareon': "Eevee's evolution", 'Gengar': "Gastly's 2'nd evolution", 'Golem': "Geodude's 2'nd evolution", 'Gyarados': "Magikarp's evolution", 'Jolteon': "Eevee's evolution", 'Kabutops': "Kabuto's evolution", 'Machamp': "Machop's 2'nd evolution", 'Marowak': "Cubone's evolution", 'Muk': "Grimer's evolution", 'Nidoking': "NidoranM's evolution", 'Nidoqueen': "Nidorina's evolution", 'Ninetales': "Vulpix's evolution", 'Raichu': "Pikachu's evolution", 'Rhydon': "Rhyhorn's evolution", 'Snorlax': '', 'Vaporeon': "Eevee's evolution", 'Venusaur': "Bulbasaur's 2'nd evolution", 'Zapdos': '', 'Moltres': '', 'Mewtwo': '', 'Mew': '', 'Dragonite': "Dratini's 2'nd evolution", 'Ditto': '', 'Articuno': ''}

GenerationProbabilities = {"Common": '600',
                            "Uncommon": '230',
                            "Rare": '120',  # key - веротность выпаения покемона, value -  list с именами покемонов
                            "SuperRare": '30',
                            "Epic": '19',  # вероятности должны быть написаны целыми числами
                            "Legendary":'1'}

POKEMON_BY_TYPE = {
    'Normal⭕': ['Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Jigglypuff', 'Wigglytuff', 'Meowth', 'Persian', 'Doduo', 'Dodrio', 'Lickitung', 'Chansey', 'Kangaskhan', 'Tauros', 'Ditto', 'Eevee', 'Porygon', 'Snorlax'],
    'Fire🔥': ['Charmander', 'Charmeleon', 'Charizard', 'Vulpix', 'Ninetales', 'Growlithe', 'Arcanine', 'Ponyta', 'Rapidash', 'Magmar', 'Flareon'],
    'Water💧': ['Squirtle', 'Wartortle', 'Blastoise', 'Psyduck', 'Golduck', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Tentacool', 'Tentacruel', 'Slowpoke', 'Slowbro', 'Seel', 'Dewgong', 'Shellder', 'Cloyster', 'Krabby', 'Kingler', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Magikarp', 'Gyarados', 'Lapras', 'Vaporeon', 'Omastar'],
    'Electric⚡': ['Pikachu', 'Raichu', 'Magnemite', 'Magneton', 'Voltorb', 'Electrode', 'Electabuzz', 'Jolteon'],
    'Grass🌿': ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Exeggcute', 'Exeggutor', 'Tangela'],
    'Ice❄️': ['Dewgong', 'Cloyster', 'Jynx', 'Lapras', 'Articuno'],
    'Fighting🥊': ['Mankey', 'Primeape', 'Poliwrath', 'Machop', 'Machoke', 'Machamp', 'Hitmonlee', 'Hitmonchan'],
    'Poison☠️': ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Weedle', 'Kakuna', 'Beedrill', 'Ekans', 'Arbok', 'Nidoran♀', 'Nidorina', 'Nidoqueen', 'Nidoran♂', 'Nidorino', 'Nidoking', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Venonat', 'Venomoth', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Grimer', 'Muk', 'Gastly', 'Haunter', 'Gengar', 'Koffing', 'Weezing'],
    'Ground🌱': ['Sandshrew', 'Sandslash', 'Nidoqueen', 'Nidoking', 'Diglett', 'Dugtrio', 'Geodude', 'Graveler', 'Golem', 'Onix', 'Cubone', 'Marowak', 'Rhyhorn', 'Rhydon'],
    'Flying🪽': ['Charizard', 'Butterfree', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Spearow', 'Fearow', 'Zubat', 'Golbat', 'Farfetch’d', 'Doduo', 'Dodrio', 'Scyther', 'Gyarados', 'Aerodactyl'],
    'Psychic🌀': ['Abra', 'Kadabra', 'Alakazam', 'Slowpoke', 'Slowbro', 'Drowzee', 'Hypno', 'Exeggcute', 'Exeggutor', 'Mr. Mime', 'Jynx', 'Mewtwo', 'Mew'],
    'Bug🐛': ['Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Scyther', 'Pinsir'],
    'Rock🪨': ['Geodude', 'Graveler', 'Golem', 'Onix', 'Rhyhorn', 'Rhydon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl'],
    'Ghost👻': ['Gastly', 'Haunter', 'Gengar'],
    'Dragon🐉': ['Dratini', 'Dragonair', 'Dragonite'],
    'Dark🌑': [], # В первом поколении не было темного типа
    'Steel🛡️': [], # В первом поколении не было стального типа
    'Fairy🧚': ['Clefairy', 'Clefable', 'Jigglypuff', 'Wigglytuff', 'Mr. Mime']
}

POKEMON_CATCH_SUCCESS_RATES = {
    'Common': 70,
    'Uncommon': 50,
    'Rare': 30,
    'SuperRare': 20,
    'Epic': 10,
    'Legendary': 5
}

