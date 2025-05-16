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

from ingestion.data_processing import calculate_type_effectiveness


class TeamBuilder:
    def __init__(self, use_babies: bool, use_legends: bool, file_to_use: str, preferences: dict[str, bool]):
        self.use_babies: bool = use_babies
        self.use_legends: bool = use_legends
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
        if self.use_babies:
            for name, info in self.data.items():
                if info['evo_weight'] == 0.0:
                    temp.update({name: info})

                self.data = temp
            return

        # filter the data to the default information: any Pokémon with an evo_weight > 0.0; i.e., exclude baby Pokémon
        for name, info in self.data.items():
            # if not using legends, skip to the next entry
            if not self.use_legends and info['is_legend_or_mythical']:
                continue

            if info['evo_weight'] > 0.0:
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

    def build_team(self) -> list[str]:
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
                print(f'Role {role} not found in grouped.groups roles: {list(grouped.groups.keys())}')
                continue

            # shuffles the rows of the cluster
            candidates = grouped.get_group(role).sample(frac=1)

            for _, row in candidates.iterrows():
                if len(team) >= 6:
                    break

                print(f"Trying role: {role} with {len(candidates)} candidates.")

                name: str = row['name']
                types: list[str] = row['types'] if isinstance(row['types'], list) else [row['types']]

                # calculate the potential weaknesses
                potential_types: list[list[str]] = team_types + [types]
                weaknesses = self.get_team_weaknesses(potential_types)

                # if a specific weakness will have more than 2 overlaps, don't add the Pokémon to the team
                if any(count > 2 for count in weaknesses.values()):
                    print(f"Skipping {name} due to excessive shared weaknesses: {weaknesses}")
                    continue

                print(f'Added {name} to the team')
                team.append(name)
                team_types.append(types)
                break

        # a fallback system to include other clusters if there is room in the team
        if len(team) < 6:
            remaining: DataFrame = self.df_encoded[~self.df_encoded['name'].isin(team)]
            additional: list = remaining.sample(n=6 - len(team))['name'].tolist()
            team.extend(additional)

        if not team:
            print('Warning: no Pokemon added to the team')

        return team

    def visualize(self) -> None:
        """
        Used to visualize the Elbow Method of determining appropriate cluster sizing. Not necessary to use for the
        application, but to understand how to improve it.
        """
        inertias = []
        k_range = range(1, 30)

        # Use only numeric columns
        numeric_columns = self.df_encoded.select_dtypes(include='number').columns
        features = self.df_encoded[numeric_columns]

        for k in k_range:
            model = KMeans(n_clusters=k, random_state=42)
            model.fit(features)
            inertias.append(model.inertia_)

        plt.plot(k_range, inertias, marker='o')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia (Distortion)')
        plt.title('Elbow Method for Optimal k')
        plt.grid(True)
        plt.show()

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


if __name__ == '__main__':
    preferences: dict[str, bool] = {
        'more_offensive': False,
        'more_defensive': False,
        'more_balanced': True
    }

    tb: TeamBuilder = TeamBuilder(False, False,
                                  '../data/pokemon_data/gen_1_data.json', preferences)
    tb.create_df()
    tb.encode_and_normalize()
    tb.clustering()
    tb.categorize()

    # tb.print_clusters()

    team: list[str] = tb.build_team()
    print(f'Generated team: {team}')
    print(f"Team size: {len(team)}")
