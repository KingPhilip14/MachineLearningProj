import math
import random
from collections import Counter

import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt

import json

import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from utils import get_role_description, calculate_type_effectiveness


class TeamBuilder:
    def __init__(self, use_babies: bool, use_legends: bool, file_to_use: str, preferences: dict[str, bool]):
        self.using_babies: bool = use_babies
        self.using_legends: bool = use_legends
        self.file_to_use: str = file_to_use
        self.data = dict()

        with open(file_to_use, 'r') as file:
            self.data = json.load(file)
            self.filter_data()

        self.df: DataFrame = pd.DataFrame()
        self.df_encoded: DataFrame = pd.DataFrame()

        self.preferences: dict[str, bool] = {
            'more_offensive': preferences['more_offensive'],
            'more_defensive': preferences['more_defensive'],
            'more_balanced': preferences['more_balanced'],
        }

    def filter_data(self) -> None:
        temp: dict = dict()

        # if using baby Pokémon, filter the data to those only and return that data
        if self.using_babies:
            # Some Pokémon are banned from the Little Cup format, so they will be excluded
            banned_list: list[str] = ['Scyther', 'Sneasel', 'Yanma', 'Tangela', 'Swirlix', 'Gligar', 'Meditite',
                                      'Murkrow', 'Misdreavus', 'Drifloon', 'Porygon', 'Cutiefly', 'Gothita']

            for name, info in self.data.items():
                # Exclude banned Pokémon
                if name in banned_list:
                    continue

                if info['evo_weight'] == 0.0:
                    temp.update({name: info})

                self.data = temp
            return

        # filter the data to the default information: any Pokémon with an evo_weight > 0.0; i.e., exclude baby Pokémon
        for name, info in self.data.items():
            # if not using legends, skip to the next entry
            if not self.using_legends and info['is_legend_or_mythical']:
                continue

            # always include fully evolved forms; exclude any Pokémon that are babies or have a low BST
            if info['evo_weight'] == 1.0 or (info['evo_weight'] > 0.0 and info['bst'] >= 350):
                temp.update({name: info})

        self.data = temp

    def create_df(self) -> None:
        """
        Collects the data of every Pokémon in the JSON file used and converts it to a dataframe.
        """
        df_entries: list = []

        for name, info in self.data.items():
            df_entry = {
                'name': name,
                'bst': info['bst'],
                'hp': info['hp'],
                'attack': info['attack'],
                'defense': info['defense'],
                'special-attack': info['special-attack'],
                'special-defense': info['special-defense'],
                'speed': info['speed'],
                'role': info['role'],
                'is_fully_evolved': info['is_fully_evolved'],
                'evo_weight': info['evo_weight'],
                'types': [info['type_1']] if not info['type_2'] else [info['type_1'], info['type_2']],
            }

            df_entries.append(df_entry)

        self.df = pd.DataFrame(df_entries)

    def encode_and_normalize(self) -> None:
        """
        Encodes and normalizes the data collected in the dataframe.

        Encoded features:
            - Role
            - Is Fully Evolved

        Normalized features:
            - HP
            - Attack
            - Defense
            - Special Attack
            - Special Defense
            - Speed
        """

        # keep the names and types separated from the df_encoded DataFrame
        names: DataFrame = self.df['name']
        types: DataFrame = self.df['types']

        # encode features of the dataframe using one-hot encoding
        self.df_encoded: DataFrame = pd.get_dummies(self.df.drop(columns=['name']), columns=['role'], dtype=int)
        self.df_encoded['is_fully_evolved'] = self.df_encoded['is_fully_evolved'].astype(int)

        # normalize features
        sc = StandardScaler()
        stat_columns = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed', 'bst']
        self.df_encoded[stat_columns] = sc.fit_transform(self.df_encoded[stat_columns])

        # add the names and types back for later
        self.df_encoded['name'] = names
        self.df_encoded['types'] = types

    def clustering(self) -> None:
        # determine columns that need to be dropped to fit the data without crashing
        drop_columns: list[str] = ['name', 'types']

        cluster_features = self.df_encoded.drop(columns=drop_columns)

        # used for creating a dynamically adjustable number of clusters
        data_size: int = len(self.df_encoded)

        # the following formula will adjust the number of k, capping at 15 to reduce extra noise
        k = min(15, max(4, round(math.log2(data_size) + data_size / 50)))

        k_means = KMeans(n_clusters=k, random_state=42)
        self.df_encoded['cluster'] = k_means.fit_predict(cluster_features)

    def name_clusters(self, row) -> str:
        """
        Assigns cluster names using by analyzing the mean of the stats of the Pokémon in a cluster and its role.
        """
        # get the stats from the cluster
        hp = row['hp']
        attack = row['attack']
        defense = row['defense']
        special_attack = row['special-attack']
        special_defense = row['special-defense']
        speed = row['speed']

        # determine thresholds to use for labeling
        evo_weight: float = row.get('evo_weight', 1.0)
        support_score: float = row.get('role_Utility/Support', 0)
        hp_threshold: float = 0.5
        wall_threshold: float = 0.60
        sweeper_speed_threshold: float = 0.50
        offense_threshold: float = 0.60
        mixed_threshold: float = 0.40
        speed_threshold: float = 0.50

        # determine if the cluster is Pokémon that can use an Eviolite (a very useful item competitively)
        # this only applies to partially evolved Pokémon (i.e., Pokémon with an evo_weight of 0.5)
        if evo_weight == 0.5:
            return 'Eviolite User'

        # determine "Sweeper" archetypes
        if attack > offense_threshold and speed > sweeper_speed_threshold:
            return 'Physical Sweeper'

        if special_attack > offense_threshold and speed > sweeper_speed_threshold:
            return 'Special Sweeper'

        # determine "Attacker" archetypes (still good attacking Pokémon, but not fast enough to be a sweeper)
        if attack > offense_threshold:
            return 'Physical Attacker'

        if special_attack > offense_threshold:
            return 'Special Attacker'

        if attack > mixed_threshold and special_attack > mixed_threshold:
            return 'Mixed Attacker'

        # determine "Wall" archetype
        if defense > wall_threshold and special_defense < 0.2:
            return 'Physical Wall'

        if special_defense > wall_threshold and defense < 0.2:
            return 'Special Wall'

        if defense > wall_threshold and special_defense > wall_threshold:
            return 'Bulky Wall'

        # determine if Bulky based on HP without high defenses
        if hp > hp_threshold:
            return 'Bulky'

        # determine if speedy without much offense
        if speed > speed_threshold:
            return 'Speedster'

        # determine if Utility/Support
        if support_score > 0.35:
            return 'Utility/Support'

        # default edge case
        return 'Versatile'

    def categorize(self) -> None:
        """
        Assigns each Pokémon to a cluster to categorize them.
        :return:
        """
        # assign category names to each Pokémon in a cluster
        self.df_encoded['cluster_name'] = self.df_encoded.apply(self.name_clusters, axis=1)

    def print_clusters(self) -> None:
        """
        Prints the different named clusters and all Pokémon in them. Primarily used for debugging purposes.
        """
        for name, group in self.df_encoded.groupby('cluster_name'):
            print(f'{name}: {group["name"].tolist()}\n')

    def get_team_weaknesses(self, team_types: list[list[str]]) -> Counter:
        """
        By iterating through the team types, the amount of overlapping weaknesses is calculated.
        :param team_types:
        """
        weaknesses: Counter = Counter()

        for types in team_types:
            effectiveness = calculate_type_effectiveness(types[0], types[1] if len(types) > 1 else '')

            for type_, multiplier in effectiveness.items():
                if multiplier > 1.0:
                    weaknesses[type_] += 1

        return weaknesses

    def build_team(self) -> tuple[list[str], DataFrame, list[list[str]]]:
        """
        Creates a team of Pokémon for the end user to use. The team is created based on the cluster roles and inputs
        from the user.
        """

        team: list[str] = []
        team_types: list[list[str]] = []

        grouped = self.df_encoded.groupby('cluster_name')
        preferred_roles: list[str] = self.__convert_preferences()

        # shuffle the preferences to not have the same result of clusters frequently
        random.shuffle(preferred_roles)

        for role in preferred_roles:
            if len(team) >= 6:
                break

            # checks if a role is not in the groups of clusters; some clusters may not exist depending on the data file
            if role not in grouped.groups:
                continue

            # shuffles the rows of the cluster
            candidates = grouped.get_group(role).sample(frac=1)

            for _, row in candidates.iterrows():
                if len(team) >= 6:
                    break

                name: str = row['name']
                types: list[str] = row['types'] if isinstance(row['types'], list) else [row['types']]

                # calculate the potential weaknesses
                potential_types: list[list[str]] = team_types + [types]
                weaknesses = self.get_team_weaknesses(potential_types)

                # if a specific weakness will have more than 2 overlaps, don't add the Pokémon to the team
                if any(count > 2 for count in weaknesses.values()):
                    continue

                team.append(name)
                team_types.append(types)
                break

        # a fallback system to include other clusters if there is room in the team
        if len(team) < 6:
            remaining: DataFrame = self.df_encoded[~self.df_encoded['name'].isin(team)]
            additional: list = remaining.sample(n=6 - len(team))['name'].tolist()
            team.extend(additional)

        if not team:
            print('Warning: no Pokémon added to the team')

        # add the role the Pokémon will fulfill next to its name for the output
        team_with_details: list[str] = []

        # build a detailed string for each Pokémon in the generated team
        for name in team:
            role_row: DataFrame = self.df_encoded[self.df_encoded['name'] == name]
            role: str = role_row.iloc[0]['cluster_name'] if not role_row.empty else 'Versatile'

            info = self.data.get(name)

            # get the type(s) of the Pokémon
            type_1: str = info.get('type_1', '')
            type_2: str = info.get('type_2', '')
            type_str: str = f'{type_1.title()}/{type_2.title()}' if type_2 else type_1.title()

            # get the stats of the Pokémon
            stats: dict[str, int] = {
                'hp': info['hp'],
                'attack': info['attack'],
                'defense': info['defense'],
                'special-attack': info['special-attack'],
                'special-defense': info['special-defense'],
                'speed': info['speed'],
                'bst': info['bst'],
            }

            # get all abilities
            abilities: list[str] = info['abilities']
            abilities_str: str = ', '.join(ability.title().replace('-', ' ') for ability in abilities)

            details: str = (
                f'{name.title()} ({type_str}) - {role}\n'
                f'Role Description: {get_role_description(role)}\n'
                f'\tStats:\n'
                f'\t\tHP: {stats["hp"]}\n'
                f'\t\tAttack: {stats["attack"]}\n'
                f'\t\tDefense: {stats["defense"]}\n'
                f'\t\tSpecial Attack: {stats["special-attack"]}\n'
                f'\t\tSpecial Defense: {stats["special-defense"]}\n'
                f'\t\tSpeed: {stats["speed"]}\n'
                f'\t\tBST: {stats["bst"]}\n'
                f'\tAbilities: {abilities_str}'
            )

            team_with_details.append(details)

        # build a DataFrame to use later
        team_df: DataFrame = self.df_encoded[self.df_encoded['name'].isin(team)]

        team_types: list[list[str]] = [
            [self.data[name]['type_1']] if not self.data[name]['type_2']
            else [self.data[name]['type_1'], self.data[name]['type_2']]
            for name in team
        ]

        return team_with_details, team_df, team_types

    def __convert_preferences(self) -> list[str]:
        """
        Uses the dict of preferences to determine the returned list of strings. The returned list will indicate how many
        Pokémon of a particular role are added to the final team composition.
        """
        if self.preferences['more_offensive']:
            return ['Physical Sweeper', 'Special Sweeper', 'Physical Sweeper', 'Special Sweeper', 'Utility/Support',
                    'Mixed Attacker', 'Physical Attacker', 'Special Attacker', 'Speedster', 'Bulky', 'Bulky Wall']

        if self.preferences['more_defensive']:
            return ['Physical Wall', 'Special Wall', 'Physical Wall', 'Special Wall', 'Bulky', 'Bulky Wall',
                    'Physical Attacker', 'Special Attacker', 'Versatile', 'Utility/Support', 'Eviolite User']

        if self.preferences['more_balanced']:
            return ['Physical Sweeper', 'Special Sweeper', 'Physical Wall', 'Special Wall', 'Mixed Attacker',
                    'Speedster', 'Bulky', 'Bulky Wall', 'Utility/Support', 'Eviolite User', 'Versatile']

    def get_team_synergy_desc(self, team_df: pd.DataFrame, team_types: list[list[str]]) -> str:
        """
        A description of the team's synergy and how each Pokémon complements each other is returned to give the user a
        better understand of how they may be able to use their team.
        :param team_df:
        :param team_types:
        """
        comments: list[str] = []

        # look at type coverage
        all_weaknesses: Counter = Counter()

        for types in team_types:
            effectiveness = calculate_type_effectiveness(types[0], types[1] if len(types) > 1 else '')
            for t, mult in effectiveness.items():
                if mult > 1.0:
                    all_weaknesses[t] += 1

        # find if the team has many overlapping weaknesses that would be concerning
        weak_types: list[str] = [f'{type_}' for type_, count in all_weaknesses.items() if count >= 2]

        if weak_types:
            formatted_types: str = ', '.join(type_[0].upper() + type_[1:] for type_ in weak_types)
            comments.append(f'The team has overlapping weaknesses to: {formatted_types}. Be mindful of these!')
        else:
            comments.append('The team has good type coverage, so no major weaknesses are shared.')

        # look at stat synergy
        average_stats = team_df[['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']].mean()

        if average_stats['speed'] > 0.35:
            comments.append('This team has many fast Pokémon. Use that speed to your advantage as you move first.')
        elif average_stats['defense'] > 0.35 and average_stats['special-defense'] > 0.35:
            comments.append(
                'Playing defensively with this team is how you\'ll find success. Use your defenses to control '
                'the pace of the match!')
        elif average_stats['attack'] + average_stats['special-attack'] > .50:
            comments.append(
                'The offensive pressure from this team will be expected. End the match quickly and watch for '
                'your lack of defenses.')
        else:
            comments.append('This team is well balanced overall. Do what you can with it!')

        return '\n'.join(comments)

    def generate_team(self) -> list[str]:
        """
        Combines all methods used to build a team, then builds a string to print to the user for what their new team
        is.
        """
        self.create_df()
        self.encode_and_normalize()
        self.clustering()
        self.categorize()

        built_team_result: tuple[list[str], DataFrame, list[list[str]]] = self.build_team()

        team_details: list[str] = built_team_result[0]
        team_df: DataFrame = built_team_result[1]
        team_types: list[list[str]] = built_team_result[2]

        team_comments: str = self.get_team_synergy_desc(team_df, team_types)

        print(f'----- Generated Team -----\n\n' + '\n\n'.join(team_details))
        print(f'\nTeam Synergy Notes:\n{team_comments}')

        return team_details
