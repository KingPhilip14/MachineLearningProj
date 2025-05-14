import json

import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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
                'highest_move_categories': '-'.join(sorted(info['highest_move_categories'])),
            }

            df_entries.append(df_entry)

        self.df = pd.DataFrame(df_entries)

    def encode_and_normalize(self) -> None:
        """
        Encodes and normalizes the data collected in the dataframe.

        Encoded features:
            - Pokémon Role
            - Highest Move Categories

        Normalized features:
            - HP
            - Attack
            - Defense
            - Special Attack
            - Special Defense
            - Speed
        """

        # encode features of the dataframe
        self.df_encoded: DataFrame = pd.get_dummies(self.df, columns=['role'])

        # encode the move categories too
        move_categories = ['status', 'physical', 'special']

        for category in move_categories:
            self.df_encoded[category] = self.df['highest_move_categories'].apply(lambda x: int(category in x))

        # normalize features
        scaler = StandardScaler()
        stat_columns = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']

        # drop the name column to only fit based on the numeric values
        self.df_encoded[stat_columns] = scaler.fit_transform(self.df_encoded[stat_columns])

    def clustering(self) -> None:
        # determine columns that need to be dropped to fit the data without crashing
        drop_columns: list[str] = ['name', 'highest_move_categories']

        k_means = KMeans(n_clusters=10, random_state=42)
        self.df_encoded['cluster'] = k_means.fit_predict(self.df_encoded.drop(columns=drop_columns))

    def name_clusters(self) -> None:
        """
        Gives names to each cluster group based on the dominant role in each cluster.
        """
        role_columns = [col for col in self.df_encoded.columns if col.startswith('role_')]

        # calculate average role presence per cluster
        cluster_profiles = self.df_encoded.groupby('cluster')[role_columns].mean()

        print(f'\nCluster Role Averages:\n{cluster_profiles}')

        # assign the most common role to each cluster
        cluster_names = {}
        for cluster_id_, row in cluster_profiles.iterrows():
            dominant_role_col = row.idxmax()
            cluster_names[cluster_id_] = dominant_role_col.replace('role_', '').replace('_', ' ')

        # map cluster ID to name
        self.df_encoded['cluster_name'] = self.df_encoded['cluster'].map(cluster_names)

    # def name_clusters(self) -> None:
    #     """
    #     Gives names to each cluster group based on the average stats and roles of the Pokémon.
    #     """
    #     # get average stats and role composition per cluster
    #     stat_columns = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    #     role_columns = [col for col in self.df_encoded.columns if col.startswith('role_')]
    #     move_columns = ['status', 'physical', 'special']
    #
    #     # combine the numeric columns
    #     profile_columns = stat_columns + role_columns + move_columns
    #     cluster_profiles = self.df_encoded.groupby('cluster')[profile_columns].mean()
    #
    #     print(f'\nCluster Profiles\n{cluster_profiles}')
    #
    #     # assign cluster names
    #     cluster_names = {
    #         0: "Physical Sweepers",
    #         1: "Bulky Walls",
    #         2: "Special Sweepers",
    #         3: "Utility/Support",
    #         4: "Mixed Attackers",
    #         5: "Balanced All-Rounders"
    #     }
    #
    #     # add labels to the dataframe
    #     self.df_encoded['cluster_name'] = self.df_encoded['cluster'].map(cluster_names)

    def override_cluster(self, row):
        """
        Overrides blatantly misclassified Pokémon to correct mistakes. This is done by looking at the Bast Stat Total
        (BST) and the attacking stats of the Pokémon.
        """
        if row['bst'] < 300 and row['status'] == 1 and row['attack'] < 40 and row['special-attack'] < 40:
            return 'Utility/Support'

        return row['cluster_name']


if __name__ == '__main__':
    tb: TeamBuilder = TeamBuilder(False, False, '../data/pokemon_data/gen_1_data.json')
    tb.create_df()
    tb.encode_and_normalize()
    tb.clustering()
    tb.name_clusters()

    tb.df_encoded['cluster_name_corrected'] = tb.df_encoded.apply(tb.override_cluster, axis=1)

    # for cluster_id in sorted(tb.df_encoded['cluster'].unique()):
    #     subset = tb.df_encoded[tb.df_encoded['cluster'] == cluster_id]
    #     label_counts = subset['cluster_name_corrected'].value_counts()
    #     dominant_label = label_counts.idxmax()
    #     names = subset['name'].tolist()
    #     print(f'Cluster {cluster_id} ({dominant_label}): {names}\n')

    for cluster_id in sorted(tb.df_encoded['cluster'].unique()):
        subset = tb.df_encoded[tb.df_encoded['cluster'] == cluster_id]
        original_label = tb.df_encoded[tb.df_encoded['cluster'] == cluster_id]['cluster_name'].iloc[0]
        corrected_names = subset[subset['cluster_name'] != subset['cluster_name_corrected']]['name'].tolist()
        all_names = subset['name'].tolist()

        print(f'Cluster {cluster_id} ({original_label}):')
        print(f'  Pokémon: {all_names}')
        if corrected_names:
            print(f'  Manually overridden to another label: {corrected_names}')
        print()

