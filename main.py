from utils import input_generation
from ingestion.data_collection import *


if __name__ == '__main__':
    print('Welcome to the ML Pokemon Team Generator!')
    user_input_collection: tuple[str, list[int]] = input_generation()
    collect_data(user_input_collection[0], user_input_collection[1])
