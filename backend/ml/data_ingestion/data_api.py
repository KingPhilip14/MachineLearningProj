import asyncio

import aiohttp
from tqdm import tqdm

from backend.ml.data_ingestion.base_api import BaseApi
from config import POKEMON_DATA_DIR
from utils import pokemon_data_file_exists, save_json_file, roman_to_int, get_generation_num


class DataApi(BaseApi):
    def __init__(self, filename: str = 'national', pokedex_ids: list[int] = [1]):
        super().__init__()
        self.filename: str = filename
        self.pokedex_ids: list[int] = pokedex_ids
        self.pokedex_entries: list[str] = []
        self.generation: int = get_generation_num(filename)

    async def get_generation_pokedex(self, pokedex_ids: list[int]) -> dict[str, str]:
        """
        Using the Pokédex endpoint and the list of Pokédex IDs given, a new dictionary is created combining the info of
        all Pokémon found. The first step in collecting data.
        :param pokedex_ids:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            urls: list[str] = [f'{self.base_url}pokedex/{pid}' for pid in pokedex_ids]
            pokedexes: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in urls])

        collection: dict[str, str] = dict()

        for pokedex in tqdm(pokedexes):
            for entry in pokedex['pokemon_entries']:
                species_name: str = entry['pokemon_species']['name']

                # used to include all National Pokédex Pokémon without including potential duplicates
                if species_name not in collection:
                    collection[species_name] = entry['pokemon_species']['url'][:-1]

        print('Pokémon info collected')
        return collection

    async def get_species_data(self, pokemon_species: dict[str, str]) -> dict[str, dict]:
        """
        Given the data of a Pokémon species, extra information is gathered, such as if the Pokémon is fully evolved
        and if it's a legendary or mythical. The second step in the data collection.
        :param pokemon_species:
        :return:
        """
        print('\nAdding "is_fully_evolved" to all collected Pokémon...\n')

        result: dict[str, dict] = dict()

        async with aiohttp.ClientSession() as session:
            species_jsons: list[dict] = await asyncio.gather(
                *[self.fetch_json(session, url) for url in pokemon_species.values()])

            # map each species name with its appropriate data retrieved
            species_name_map: dict[str, dict] = dict(zip(pokemon_species.keys(), species_jsons))

            # get the evolution chain URLs
            evo_urls: list[str] = [species['evolution_chain']['url'][:-1] for species in species_jsons]
            evo_chains: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in evo_urls])

            # map each species name to its evolution chain data
            evolution_map: dict[str, dict] = dict(zip(pokemon_species.keys(), evo_chains))

            for pokemon_name in tqdm(pokemon_species.keys()):
                species_json: dict = species_name_map[pokemon_name]

                evolution_chain: dict = evolution_map[pokemon_name]['chain']

                is_legend_or_mythical: bool = species_json['is_legendary'] or species_json['is_mythical']

                # a list containing the names for different forms of the species
                varieties: list[str] = [variety['pokemon']['name'] for variety in species_json['varieties']]

                evo_weight: float = 0.0

                fully_evolved: bool

                if evolution_chain['species']['name'] == pokemon_name:
                    # checks if the current Pokémon is the species; if so, check if it's fully evolved
                    fully_evolved = len(evolution_chain['evolves_to']) == 0
                else:
                    # otherwise, recursively determine if the Pokémon is fully evolved and its evo_weight
                    fully_evolved, evo_weight = self.__find_pokemon_in_chain(pokemon_name, evolution_chain)

                result[pokemon_name] = {
                    'is_fully_evolved': fully_evolved,
                    'evo_weight': 1.0 if fully_evolved else evo_weight,
                    'is_legend_or_mythical': is_legend_or_mythical,
                    'varieties': varieties,
                }

        return result

    async def get_additional_info(self, species_data: dict[str, dict]) -> dict[str, dict]:
        print('Collecting addtional info\n\n')
        output: dict[str, dict] = dict()

        async with aiohttp.ClientSession() as session:
            tasks: list[asyncio.Task] = []

            for species_name, data in tqdm(species_data.items()):
                # the default form is always first in the list
                default_form_name: str = data['varieties'][0]

                # every other form is used to determine their significance
                other_forms: list[str] = data['varieties'][1:]

                tasks.append(asyncio.create_task(self.process_forms(session, default_form_name, other_forms)))

            # get the data from all the tasks
            results: list[dict] = await asyncio.gather(*tasks)

            for entry in results:
                output.update(entry)

        return output

    async def process_forms(self, session: aiohttp.ClientSession, default_form_name: str,
                            other_forms: list[str]) -> dict[str, dict]:
        forms_data: dict[str, dict] = dict()

        default_url: str = f'{self.base_url}pokemon/{default_form_name}/'
        default_data: dict = await self.fetch_json(session, default_url)

        tasks: list[asyncio.Task] = [asyncio.create_task(self.__get_significant_forms(session, form, default_data))
                                     for form in other_forms]
        significant_form_data: list[dict[str, dict]] = await asyncio.gather(*tasks)

        for data in [default_data] + [form for form in significant_form_data if form]:
            name: str = data['name']
            move_coverage: set[str] = await self.__get_move_coverage(session, data['moves'])
            moveset: list[dict] = await self.__get_moveset(session, data['moves'])
            abilities: list[dict] = await self.__get_abilities(session, data['abilities'])

            forms_data[name] = {
                'id': data['id'],
                'species': data['species']['name'],
                'type_1': data['types'][0]['type']['name'],
                'type_2': data['types'][1]['type']['name'] if len(data['types']) > 1 and data['types'][1]['type'][
                    'name'] is not None else '',
                'bst': sum([stat['base_stat'] for stat in data['stats']]),
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
                'special-attack': data['stats'][3]['base_stat'],
                'special-defense': data['stats'][4]['base_stat'],
                'speed': data['stats'][5]['base_stat'],
                'abilities': abilities,
                'moveset': moveset,
                'move_coverage': list(move_coverage),
                'highest_move_categories': self.__get_most_common_move_categories(list(move_coverage)),
            }

        return forms_data

    async def __get_significant_forms(self, session: aiohttp.ClientSession, form_name: str,
                                      default_form_data: dict) -> dict[str, dict] | None:
        """
        Returns data for the given form if it is considered significant. Significant forms are forms that:
        - Are a mega or gmax form
        - Are not solely a cosmetic change
        - Change the Pokémon's stats, ability(ies), typing, or moveset
        :param session:
        :param form_name:
        :param default_form_data:
        """
        form_suffixes: list[str] = ['mega', 'primal', 'gmax', 'alola', 'hisui', 'galar']

        valid_forms_in_gens: dict[int, list[str]] = {
            6: ['mega', 'primal'],
            7: ['alola', 'mega', 'primal'],
            8: ['hisui', 'galar', 'alola', 'gmax'],
            9: ['hisui', 'galar', 'alola']
        }

        form_url: str = f'{self.base_url}pokemon/{form_name}/'
        form_data: dict[str, dict] = await self.fetch_json(session, form_url)

        form_meta_url: str = f'{self.base_url}pokemon-form/{form_name}'
        form_meta_data: dict[str, dict] = await self.fetch_json(session, form_meta_url)

        version_group_url: str = form_meta_data['version_group']['url']

        # find the form's generation through the endpoints
        version_data: dict[str, dict] = await self.fetch_json(session, version_group_url)

        form_generation: str = version_data['generation']['name']
        form_generation_num: int = roman_to_int(form_generation.split('-')[-1])

        # check if the stats, type(s), abilities match, and movesets match
        stats_equal: bool = default_form_data['stats'] == form_data['stats']
        typing_equals: bool = default_form_data['types'] == form_data['types']
        abilities_equal: bool = default_form_data['abilities'] == form_data['abilities']
        movesets_equal: bool = default_form_data['moves'] == form_data['moves']

        # if collecting date for national dex, only check for cosmetic forms
        if self.generation == -1 and stats_equal and typing_equals and abilities_equal and movesets_equal:
            print(f'Cannot add '
                  f'the "{form_name}" form because it is either cosmetic or does not meet the significance criteria.')
            return None

        if self.generation == -1:
            return form_data

        # if the form of the Pokémon comes after the generation currently in use, skip it
        # (e.g., Hisuian Zorua (gen 8) cannot be used in Unova (gen 5))
        if self.generation < form_generation_num and self.generation != -1:
            print(f'Cannot add {form_name} because it didn\'t exist before generation {self.generation}')
            return None

        # # if the form has a suffix (i.e., 'mega', 'gmax', etc.), store the string
        form_suffix: str = ''
        for suffix in form_suffixes:
            if form_name.endswith(suffix):
                form_suffix = suffix
                break

        # if there is a form suffix that is valid, return it immediately
        if form_suffix and form_suffix in valid_forms_in_gens.get(self.generation, []):
            return form_data
        elif form_suffix and form_suffix not in valid_forms_in_gens.get(self.generation, []):
            # if there is a form suffix that is not valid, return None immediately
            print(f'Cannot add {form_name} because it is not a valid form in generation {self.generation}')
            return None

        # if the form doesn't change anything noteworthy, it's insignificant
        if stats_equal and typing_equals and abilities_equal and movesets_equal:
            print(f'Cannot add the "{form_name}" form because it is either cosmetic or is not significance criteria.')
            return None

        return form_data

    async def __get_move_coverage(self, session: aiohttp.ClientSession, moves: list[dict]) -> set:
        move_urls: list[str] = [move['move']['url'][:-1] for move in moves]
        move_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in move_urls])

        return {f'{move['type']['name']} {move['damage_class']['name']}' for move in move_data}

    async def __get_moveset(self, session: aiohttp.ClientSession, moves: list[dict]) -> list[dict]:
        move_urls: list[str] = [move['move']['url'][:-1] for move in moves]
        move_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in move_urls])

        collected_data: list[dict] = []

        # collecting the desired data from each move from the data
        for move in move_data:
            to_add: dict[str, dict] = {
                move['name']:
                    {
                        'id': move['id'],
                        'damage_class': move['damage_class']['name'],
                        'type': move['type']['name'],
                        'accuracy': move['accuracy'],
                        'power': move['power'],
                        'pp': move['pp'],
                        'priority': move['priority']
                    }
            }

            collected_data.append(to_add)

        return collected_data

    async def __get_abilities(self, session: aiohttp.ClientSession, abilities: list[dict]):
        ability_urls: list[str] = [ability['ability']['url'][:-1] for ability in abilities]
        ability_data: list[dict] = await asyncio.gather(*[self.fetch_json(session, url) for url in ability_urls])

        collected_data: list[dict] = []
        to_add: dict[str, dict]

        # collecting the desired data from each move from the data
        for ability in ability_data:
            try:
                to_add = {
                    ability['name']:
                        {
                            'id': ability['id'],
                            'name': ability['name'],
                            'short_desc': [entry['short_effect'] for entry in ability['effect_entries']
                                           if entry['language']['name'] == 'en'][0],
                            'effect_desc': [entry['effect'] for entry in ability['effect_entries']
                                            if entry['language']['name'] == 'en'][0],
                            'flavor_text': [entry['flavor_text'] for entry in ability['flavor_text_entries']
                                            if entry['language']['name'] == 'en'][0],
                        }
                }

            except IndexError:
                print(
                    f'Cannot add ability effect description or short description for ability "{ability["name"]}" because getting its English effect description failed\n'
                    f'Adding empty strings for descriptions instead.instead.')

                to_add = {
                    ability['name']:
                        {
                            'id': ability['id'],
                            'name': ability['name'],
                            'short_desc': '',
                            'effect_desc': '',
                            'flavor_text': [entry['flavor_text'] for entry in ability['flavor_text_entries']
                                            if entry['language']['name'] == 'en'][0],
                        }
                }

            collected_data.append(to_add)

        return collected_data

    def __get_most_common_move_categories(self, moves: list[str]) -> list[str]:
        categories: dict[str, int] = {
            'physical': 0,
            'special': 0,
            'status': 0
        }

        for move in moves:
            category: str = move.split()[1]

            if category in categories:
                categories[category] += 1

        maximum: int = max(categories.values())

        # return the move categories that equal the maximum number of appearances
        return [key for key, value in categories.items() if value == maximum]

    def __combine_data(self, species_data: dict[str, dict], pokemon_data: dict[str, dict]) -> dict[str, dict]:
        """
        Adds the data from more_info to the given add_to dict. The final step in data collection,
        :param species_data:
        :param pokemon_data:
        :return:
        """
        print('Combining extra info to species data\n\n')
        output: dict[str, dict] = dict()

        # add the species data to the individual Pokémon's data
        for pokemon_name, data in tqdm(pokemon_data.items()):
            pokemon_species_name: str = data['species']

            # create a new entry for the output by combining the species data with the individual Pokémon's data
            output.update({pokemon_name: data | species_data[pokemon_species_name]})

        return output

    def __find_pokemon_in_chain(self, pokemon_name: str, chain: dict,
                                evo_weight: float = 0.0) -> tuple[bool, float] | None:
        """
        Moves up the chained JSON objects to find the given Pokémon. Returns if that Pokémon is fully evolved or not
        (single-stage Pokémon count as fully evolved). If a Pokémon is partially evolved, its weight will be 0.5.
        :param pokemon_name:
        :param chain:
        :param evo_weight:
        """
        current_name = chain['species']['name']

        # if the current Pokémon is the one to look for; the edge case if statement
        if current_name == pokemon_name:
            if len(chain['evolves_to']) == 0:
                # if it has no further evolutions, it's fully evolved
                return True, 1.0
            else:
                # otherwise, it's not fully evolved
                return False, evo_weight

        # move up the chain
        for evo in chain['evolves_to']:
            # adjust the evo_weight as needed to properly represent the Pokémon's stage
            next_stage = 0.5 if evo_weight == 0.0 else 1.0
            result = self.__find_pokemon_in_chain(pokemon_name, evo, next_stage)

            if result is not None:
                return result

        return None

    async def collect_data(self) -> None:
        """
        Using the filename and given Pokédex IDs, it is first determined if the given file exists. If not, methods are
        called to start the data collection. The program will pause for a few seconds after each step to not
        receive a timeout by the API.
        :return:
        """
        if pokemon_data_file_exists(self.filename):
            print(f'The file "{self.filename}" already exists containing the Pokédex data requested. '
                  f'A new one will not be created.')
            return

        collected_pokemon: dict[str, str] = await self.get_generation_pokedex(self.pokedex_ids)

        # collect the species data
        species_data: dict[str, dict] = await self.get_species_data(collected_pokemon)

        # get the extra info for each Pokémon species
        extra_info: dict[str, dict] = await self.get_additional_info(species_data)

        output: dict[str, dict] = self.__combine_data(species_data, extra_info)

        save_json_file(output, self.filename, POKEMON_DATA_DIR)
