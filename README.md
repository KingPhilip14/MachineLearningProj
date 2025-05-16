# CSCI 625 Final Project - ML Pokémon Team Builder

## How to Run the Project
1. Open the project in your editor of choice 
1. Start the `main.py` file
   1. To start it in the terminal, run ``python -m main``
   2. Otherwise, execute it with the start button in your editor

## What the Project is For
This project was for CSCI 625, Machine Learning, at North Dakota State University (NDSU). 

## The Goal
The goal of the project was to create an enjoyable way to apply Machine Learning algorithms 
to analyze data and apply it. 

Playing Pokémon is a hobby of mine, and team building is a fundamental aspect of it. This project 
analyzes the data of Pokémon and builds a somewhat viable team that could be used in battle. While it 
may not return something that would win a national championship, the teams generated are aimed to be 
fairly balanced (i.e., there aren't many overlapping weaknesses, and each Pokémon fulfills a specific 
role).

## The Process
### Data Collection
To collect data, [PokeAPI](https://pokeapi.co) was used. This API provides data on every Pokémon 
(at the time of writing this, information on every Pokémon up to generation 9 exists). 

The data collection process includes:
- Picking and choosing data to collect from the API
  - Not all the data needed was found at a single endpoint
- Creating custom JSON files with this data
- Cleaning the JSON files of any malformed data

The JSON files include information such as:
- If the Pokémon is fully evolved
- All stats (HP, Attack, Defense, etc.)
- Type interactions
  - Weaknesses
  - Resistances

### Machine Learning
The algorithm used for this project was KMeans and clustering.

To create a team that works well and provides enough balance for people to enjoy them, it's important to 
categorize Pokémon based on their stats and capabilities. Once they are categorized, depending on the 
team composition (offensive, defensive, balanced), that will determine which roles are needed and 
how many of a specific role.

The clustering was perfect for this because there are many Pokémon that fall under the same categories. 
Once they are clustered together, a selection can be made from that cluster to start the team building 
process.

## The Experience
When using the application, you will first be greeted to a list of 10 options. These options represent 
the available Pokémon for every generation; or, you can select "Everything" to use every Pokémon that 
exists.

By entering the name of one of the options (e.g., "gen 1" or "everything"), that will determine which 
JSON file is used. Each JSON contains the data for all Pokémon available for the national Pokédex of 
that generation.

The program will then check if the data files are on the local machine. If not, it will generate them 
(this is a very time-consuming process, so just download them from the repository). 

Once the data files have been verified, prompts will be asked to know what the desired team composition 
is. There are two "phases" of composition questions, what to include and how to draft a team based on 
play style.

You can choose to only include baby Pokémon (Pokémon that haven't evolved yet). If you say yes to this, 
the next question is automatically skipped. If baby Pokémon are _not_ included, you will be asked if 
you want legendaries to be included in the clusters. If not, the default setting is used (no baby 
Pokémon and no legendaries).

You can then select your play style:
- Offensive
- Defensive
- Balanced

This will affect how many Pokémon are selected from certain clusters and which clusters are used.

Your team will then be generated with brief descriptions of what each Pokémon's purpose is for the team. 
There will also be an overall team analysis at the bottom of the description to see how the team 
comes together.

## Future Plans
What is implemented right now is a fantastic start to this application. I plan to expand it in the 
future with the following goals:
- Implement a UI
- Provide better descriptions for each Pokémon and its purpose
- Add an LLM to provide better descriptions
  - This may not be done as it's not needed, but may be a nice touch
- Include Pokémon that may have been excluded
  - Pokémon with forms (Rotom, Giratina, Palafin, etc.) were excluded due to difficulties reading in the 
  data during ingestion
