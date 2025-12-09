from pydantic import BaseModel


class TeamRequest(BaseModel):
    using_little_cup: bool = False
    using_legends: bool = False
    gen_file_name: str = "national"
    composition: str = 'balanced'
