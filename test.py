from ingestion.api_functions import ApiFunctions

data = {
    "baby_trigger_item": None,
    "chain": {
        "evolution_details": [],
        "evolves_to": [
            {
                "evolution_details": [
                    {
                        "gender": None,
                        "held_item": None,
                        "item": None,
                        "known_move": None,
                        "known_move_type": None,
                        "location": None,
                        "min_affection": None,
                        "min_beauty": None,
                        "min_happiness": None,
                        "min_level": 7,
                        "needs_overworld_rain": False,
                        "party_species": None,
                        "party_type": None,
                        "relative_physical_stats": None,
                        "time_of_day": "",
                        "trade_species": None,
                        "trigger": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                        },
                        "turn_upside_down": False
                    }
                ],
                "evolves_to": [
                    {
                        "evolution_details": [
                            {
                                "gender": None,
                                "held_item": None,
                                "item": None,
                                "known_move": None,
                                "known_move_type": None,
                                "location": None,
                                "min_affection": None,
                                "min_beauty": None,
                                "min_happiness": None,
                                "min_level": 10,
                                "needs_overworld_rain": False,
                                "party_species": None,
                                "party_type": None,
                                "relative_physical_stats": None,
                                "time_of_day": "",
                                "trade_species": None,
                                "trigger": {
                                    "name": "level-up",
                                    "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                },
                                "turn_upside_down": False
                            }
                        ],
                        "evolves_to": [],
                        "is_baby": False,
                        "species": {
                            "name": "beautifly",
                            "url": "https://pokeapi.co/api/v2/pokemon-species/267/"
                        }
                    }
                ],
                "is_baby": False,
                "species": {
                    "name": "silcoon",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/266/"
                }
            },
            {
                "evolution_details": [
                    {
                        "gender": None,
                        "held_item": None,
                        "item": None,
                        "known_move": None,
                        "known_move_type": None,
                        "location": None,
                        "min_affection": None,
                        "min_beauty": None,
                        "min_happiness": None,
                        "min_level": 7,
                        "needs_overworld_rain": False,
                        "party_species": None,
                        "party_type": None,
                        "relative_physical_stats": None,
                        "time_of_day": "",
                        "trade_species": None,
                        "trigger": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                        },
                        "turn_upside_down": False
                    }
                ],
                "evolves_to": [
                    {
                        "evolution_details": [
                            {
                                "gender": None,
                                "held_item": None,
                                "item": None,
                                "known_move": None,
                                "known_move_type": None,
                                "location": None,
                                "min_affection": None,
                                "min_beauty": None,
                                "min_happiness": None,
                                "min_level": 10,
                                "needs_overworld_rain": False,
                                "party_species": None,
                                "party_type": None,
                                "relative_physical_stats": None,
                                "time_of_day": "",
                                "trade_species": None,
                                "trigger": {
                                    "name": "level-up",
                                    "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                },
                                "turn_upside_down": False
                            }
                        ],
                        "evolves_to": [],
                        "is_baby": False,
                        "species": {
                            "name": "dustox",
                            "url": "https://pokeapi.co/api/v2/pokemon-species/269/"
                        }
                    }
                ],
                "is_baby": False,
                "species": {
                    "name": "cascoon",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/268/"
                }
            }
        ],
        "is_baby": False,
        "species": {
            "name": "wurmple",
            "url": "https://pokeapi.co/api/v2/pokemon-species/265/"
        }
    },
    "id": 135
}

api = ApiFunctions()
chain = data['chain']


if __name__ == '__main__':
    api.find_pokemon_in_chain('cascoon', chain, 0.0)
