from backend.api.schemas.account_teams_response import AccountTeamsResponse


def nest_team_data(rows):
    accounts = dict()

    for row in rows:
        row_data = row._mapping

        account_id = row_data['account_id']
        team_id = row_data['team_id']

        # if the account isn't in the dict collection, add it
        if account_id not in accounts:
            accounts[account_id] = {
                'account_id': account_id,
                'username': row_data['username'],
                'teams': {}
            }

        # if the team isn't stored in the collection, add it
        if team_id not in accounts[account_id]['teams']:
            accounts[account_id]['teams'][team_id] = {
                'team_id': team_id,
                'team_name': row_data['team_name'],
                'pokemon': []
            }

        # add the Pokemon to the team
        accounts[account_id]['teams'][team_id]['pokemon'].append({
            'pit_id': row_data['pit_id'],
            'pokemon_id': row_data['pokemon_id'],
            'pokemon_name': row_data['pokemon_name'],
            'chosen_ability_id': row_data['chosen_ability_id'],
            'nickname': row_data['nickname'],
        })

    # convert the inner dicts to lists
    return [
        AccountTeamsResponse(**{'account_id': account['account_id'], 'username': account['username'],
                                'teams': list(account['teams'].values())}
                             )
        for account in accounts.values()
    ]
