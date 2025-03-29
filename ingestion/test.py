import requests


def is_fully_evolved_with_weight(pokemon_name, evolution_chain_url):
    response = requests.get(evolution_chain_url)
    if response.status_code != 200:
        return None, None  # Handle error case appropriately

    data = response.json()
    chain = data["chain"]

    # Recursive function to traverse evolution chain
    def find_pokemon_in_chain(chain, weight=0.0):
        if chain["species"]["name"] == pokemon_name:
            # If it has no further evolutions, it's fully evolved
            return len(chain["evolves_to"]) == 0, weight

        # If not found at this level, increase weight and check deeper
        for evolution in chain["evolves_to"]:
            result, new_weight = find_pokemon_in_chain(evolution, weight + 0.5)
            if result is not None:
                return result, new_weight

        return None, None

    return find_pokemon_in_chain(chain)


# Example Usage
evolution_chain_url = "https://pokeapi.co/api/v2/evolution-chain/337/"
print(is_fully_evolved_with_weight("chespin", evolution_chain_url))  # (False, 0.0)
print(is_fully_evolved_with_weight("quilladin", evolution_chain_url))  # (False, 0.5)
print(is_fully_evolved_with_weight("chesnaught", evolution_chain_url))  # (True, 1.0)
