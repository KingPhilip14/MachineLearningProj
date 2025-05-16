import json

import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class TeamBuilder:
    def __init__(self, use_babies: bool, use_legends: bool, file_to_use: str):
        self.use_babies: bool = use_babies
        self.use_legends: bool = use_legends
        self.file_to_use: str = file_to_use
        self.data = dict()

        with open(file_to_use, 'r') as file:
            self.data = json.load(file)
            self.filter_data()

        self.df: DataFrame = pd.DataFrame()
        self.df_encoded: DataFrame = pd.DataFrame()

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
            if info['evo_weight'] > 0.0:
                temp.update({name: info})

        # add legendaries to the collected data if legends were requested
        if self.use_legends:
            for name, info in self.data.items():
                if info['is_legend_or_mythical']:
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

        # keep the names separated from the df_encoded DataFrame
        names: DataFrame = self.df['name']

        # encode features of the dataframe using one-hot encoding
        self.df_encoded: DataFrame = pd.get_dummies(self.df.drop(columns=['name']), columns=['role'], dtype=int)
        self.df_encoded['is_fully_evolved'] = self.df_encoded['is_fully_evolved'].astype(int)

        # normalize features
        sc = StandardScaler()
        stat_columns = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed', 'bst']

        # drop the name column to only fit based on the numeric values
        self.df_encoded[stat_columns] = sc.fit_transform(self.df_encoded[stat_columns])

        # add the names back for display later
        self.df_encoded['name'] = names

    def clustering(self) -> None:
        # determine columns that need to be dropped to fit the data without crashing
        drop_columns: list[str] = ['name']

        cluster_features = self.df_encoded.drop(columns=drop_columns)

        k: int = 15
        k_means = KMeans(n_clusters=k, random_state=42)
        self.df_encoded['cluster'] = k_means.fit_predict(cluster_features)

    def name_clusters(self, row) -> str:
        """
        Assigns cluster names using by analyzing the mean of the stats of the Pokémon in a cluster and its role.
        """
        # get the stats from the cluster
        attack = row['attack']
        defense = row['defense']
        special_attack = row['special-attack']
        special_defense = row['special-defense']
        speed = row['speed']

        # determine thresholds to use for labeling
        support_score = row.get('role_Utility/Support', 0)
        wall_threshold = 0.75
        sweeper_speed_threshold = 0.5
        offense_threshold = 0.60
        mixed_threshold = 0.50

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

        # determine if Utility/Support
        if support_score > 0.5:
            return 'Utility/Support'

        # default edge case
        return 'Versatile'

    def visualize(self) -> None:
        inertias = []
        k_range = range(1, 20)

        for k in k_range:
            model = KMeans(n_clusters=k, random_state=42)
            model.fit(tb.df_encoded.drop(columns=['name']))
            inertias.append(model.inertia_)

        plt.plot(k_range, inertias, marker='o')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia (Distortion)')
        plt.title('Elbow Method for Optimal k')
        plt.show()


if __name__ == '__main__':
    tb: TeamBuilder = TeamBuilder(False, False, '../data/pokemon_data/gen_1_data.json')
    tb.create_df()
    tb.encode_and_normalize()
    tb.clustering()

    numeric_columns = tb.df_encoded.select_dtypes(include='number').columns
    cluster_profiles = tb.df_encoded[numeric_columns].groupby(tb.df_encoded['cluster']).mean()
    print(f'\n--- Cluster profiles ---\n{cluster_profiles}')

    # assign names to the clusters
    cluster_profiles['cluster_name'] = cluster_profiles.apply(tb.name_clusters, axis=1)

    cluster_name_map = cluster_profiles['cluster_name'].to_dict()
    tb.df_encoded['cluster_name'] = tb.df_encoded['cluster'].map(cluster_name_map)

    for name, group in tb.df_encoded.groupby('cluster_name'):
        print(f'{name}: {group["name"].tolist()}\n')
