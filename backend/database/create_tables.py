def create_tables(conn):
    """
    Creates the tables for the database.
    """
    cursor = conn.cursor()

    # drop the tables if they exist already
    drop_query = """
                 DROP TABLE IF EXISTS account;
                 DROP TABLE IF EXISTS team;
                 DROP TABLE IF EXISTS pokemon_in_team;
                 DROP TABLE IF EXISTS pokemon;
                 DROP TABLE IF EXISTS pokemon_abilities;
                 DROP TABLE IF EXISTS ability;
                 """

    cursor.execute(drop_query)

    # create the tables
    cursor.execute(create_account_table())
    cursor.execute(create_team_table())
    # cursor.execute(create_pokemon_table())
    # cursor.execute(create_pokemon_in_team_table())
    # cursor.execute(create_ability_table())
    # cursor.execute(create_pokemon_abilities_table())
    conn.commit()


def create_account_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY SERIAL,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(30) NOT NULL,
    );
    """

def create_team_table() -> str:
    return """
    CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER PRIMARY KEY SERIAL,
        FOREIGN KEY (account_id) REFERENCES account(account_id),
        total_bst INTEGER NOT NULL,
    );
    """

# def create_pokemon_table() -> str:
#     return """
#     CREATE TABLE IF NOT EXISTS pokemon(
#         pokemon_id INTEGER PRIMARY KEY,
#         nickname VARCHAR(30) NOT NULL,
#         pokemon_name VARCHAR(30) NOT NULL,
#         type_1 VARCHAR(10) NOT NULL,
#         type_2 VARCHAR(10) NOT NULL,
#         bst INTEGER NOT NULL,
#         hp INTEGER NOT NULL,
#         attack INTEGER NOT NULL,
#         defense INTEGER NOT NULL,
#         special_attack INTEGER NOT NULL,
#         special_defense INTEGER NOT NULL,
#         speed INTEGER NOT NULL,
#         role VARCHAR(30 NOT NULL,
#     );
#     """
#
# def create_pokemon_in_team_table() -> str:
#     return """
#     CREATE TABLE IF NOT EXISTS pokemon_in_team(
#         PRIMARY KEY (team_id, pokemon_id),
#         FOREIGN KEY (team_id) REFERENCES team(team_id),
#         FOREIGN KEY (pokemon_id) REFERENCES user(pokemon_id),
#     );
#     """
#
# def create_ability_table() -> str:
#     return """
#     CREATE TABLE IF NOT EXISTS ability(
#         ability_id INTEGER PRIMARY KEY,
#         ability_name VARCHAR(30) NOT NULL UNIQUE,
#         effect_desc VARCHAR(150) NOT NULL,
#     )
#     """
#
# def create_pokemon_abilities_table() -> str:
#     return """
#     CREATE TABLE IF NOT EXISTS pokemon_abilities(
#         PRIMARY KEY (pokemon_id, ability_id),
#         FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
#         FOREIGN KEY (ability_id) REFERENCES ability(ability_id)
#     );
#     """
