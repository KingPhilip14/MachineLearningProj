from pydantic import BaseModel


class TeamPrefs(BaseModel):
    # __root__: dict[str, bool] = {
    #     'more_offensive': False,
    #     'more_defensive': False,
    #     'more_balanced': True
    # }

    more_offensive: bool = False
    more_defensive: bool = False
    more_balanced: bool = True
