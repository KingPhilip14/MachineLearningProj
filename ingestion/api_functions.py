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
        # will be used to add weight to how desirable a Pokemon is; increases by 0.5 for criteria met
        weight: float = 0.0

        # get the evolution chain from the URL
        chain_url: str = requests.get(species_url).json()['evolution_chain']['url']
        evolution_chain: dict | None = requests.get(chain_url).json()['chain']

        if evolution_chain["species"]["name"] == pokemon_name:
            fully_evolved = len(evolution_chain["evolves_to"]) == 0

            # If it has no further evolutions, it's fully evolved
            result.update(
                {
                    pokemon_name: {
                        'is_fully_evolved': fully_evolved,
                        'weight': 1.0 if fully_evolved else weight,
                    }
                })
            print(f'Added {pokemon_name} to result')
            continue

        for evolution in evolution_chain["evolves_to"]:
            evo_chain_result: tuple[bool, float] | None = __find_pokemon_in_chain(pokemon_name, evolution, weight)

            if evo_chain_result is not None:
                result.update(
                    {
                        pokemon_name: {
                            'is_fully_evolved': evo_chain_result[0],
                            'weight': evo_chain_result[1]
                        }
                    })

        print(f'Added {pokemon_name} to result')

    return result


def __find_pokemon_in_chain(pokemon_name: str, chain: dict, weight: float) -> tuple[bool, float] | None:
    weight += 0.5

    if chain["species"]["name"] == pokemon_name:
        # if the Pokemon can't evolve, it's fully evolved
        fully_evolved = len(chain["evolves_to"]) == 0
        return fully_evolved, 1.0 if fully_evolved else weight

    for evolution in chain["evolves_to"]:
        # recursively climb up the chain
        result = __find_pokemon_in_chain(evolution['species']['name'], evolution, weight)
        if result is not None:
            return result

    return None


if __name__ == '__main__':
    # pokemon = get_generation_pokedex(pokedex_ids=[12, 13, 14, 15])
    pokemon = get_generation_pokedex(pokedex_ids=[2])
    # print(pokemon)

    output = is_fully_evolved(pokemon)
    print(output)
    print(f'\n\n{json.dumps(output, indent=4)}')
