import json
import requests
import os

base_url: str = 'https://pokeapi.co/api/v2/'


def get_generation_pokedex(pokedex_ids: list[int]) -> dict[str, str]:
    """
    Using the Pokedex endpoint and the list of Pokedex IDs given, a new dictionary is created combining the info of
    all Pokemon found.
    :param pokedex_ids:
    :return:
    """
    url: str = base_url + 'pokedex/'

    pokedexes: list[dict] = list()
    collection: dict[str, str] = dict()

    # collect the JSON for every Pokedex from the API
    for index, pokedex_id in enumerate(pokedex_ids):
        data: dict = requests.get(url + f'{pokedex_id}/').json()
        pokedexes.append(data)

    for pokedex in pokedexes:
        # find each Pokemon's species name
        for entry in pokedex['pokemon_entries']:
            species_name: str = entry['pokemon_species']['name']

            # if the species name is not in the output dict, add it with it's "pokemon-species/" URL
            if species_name not in collection:
                collection.update({
                    species_name: entry['pokemon_species']['url']
                })

    return collection


def is_fully_evolved(pokemon_species: dict[str, str]) -> dict[str, dict]:
    result: dict[str, dict] = dict()

    for pokemon_name, species_url in pokemon_species.items():
        print(f'Starting process for {pokemon_name}')
        fully_evolved: bool = False

        # will be used to add weight to how desirable a Pokemon is; increases by 0.5 for criteria met
        weight: float = 0.0

        # get the evolution chain from the URL
        chain_url: str = requests.get(species_url).json()['evolution_chain']['url']
        evolution_chain: dict | None = requests.get(chain_url).json()['chain']

        chain_index: int = 0

        while evolution_chain is not None:
            print(json.dumps(evolution_chain, indent=4))
            input('> ')

            # if the Pokemon doesn't evolve, consider it fully evolved and give it a weigh of 1
            if len(evolution_chain['evolves_to']) == 0:
                fully_evolved = True
                weight = 1.0
                break

            weight += 0.5

            # if on the Pokemon to look for, break out the loop
            if evolution_chain['species']['name'] == pokemon_name:
                break

            evolution_chain = evolution_chain.get(['evolves_to'][chain_index], None)

            chain_index += 1

        result.update(
            {
                pokemon_name: {
                    'is_fully_evolved': fully_evolved,
                    'weight': weight
                }
            })

        print(f'Added {pokemon_name} to result')

    return result


if __name__ == '__main__':
    pokemon = get_generation_pokedex(pokedex_ids=[12, 13, 14, 15])
    # print(pokemon)

    output = is_fully_evolved(pokemon)
    print(output)
