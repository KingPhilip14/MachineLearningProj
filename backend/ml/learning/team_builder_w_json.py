import json
import os

from pandas import DataFrame

from config import POKEMON_DATA_DIR
from team_builder import TeamBuilder


def generate_team_json(using_babies: bool, using_legends: bool, file_path: str, preferences: dict[str, bool] | None):
    tb: TeamBuilder = TeamBuilder(using_babies, using_legends, file_path, preferences)
    built_team_result: tuple[list[str], dict] = tb.generate_team()

    team_json: dict = built_team_result[1]

    return json.dumps(team_json, indent=4)


if __name__ == '__main__':
    path: str = os.path.join(POKEMON_DATA_DIR, 'national_data' + '.json')
    prefs: dict[str, bool] = {
        'more_offensive': False,
        'more_defensive': False,
        'more_balanced': True
    }

    team_data = generate_team_json(True, False, path, prefs)
    print(f'\n\nTeam json:\n{team_data}')
