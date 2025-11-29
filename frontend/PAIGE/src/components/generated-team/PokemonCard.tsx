import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import { Box, CardMedia, Typography } from "@mui/material";
import CardContent from "@mui/material/CardContent";

export default function PokemonCard() {
  const pkmnTeam = {
    Abra: {
      name: "Abra",
      hp: 30,
      attack: 10,
      defense: 10,
      "special-attack": 100,
      "special-defense": 75,
      speed: 80,
      abilities: ["ability #1", "ability #2"],
    },
    Bulbasaur: {
      name: "Bulbasaur",
      hp: 55,
      attack: 65,
      defense: 50,
      "special-attack": 65,
      "special-defense": 65,
      speed: 50,
      abilities: ["ability #1", "ability #2"],
    },
    Charizard: {
      name: "Charizard",
      hp: 80,
      attack: 90,
      defense: 80,
      "special-attack": 102,
      "special-defense": 85,
      speed: 80,
      abilities: ["ability #1", "ability #2"],
    },
    Machop: {
      name: "Machop",
      hp: 65,
      attack: 80,
      defense: 64,
      "special-attack": 30,
      "special-defense": 45,
      speed: 60,
      abilities: ["ability #1", "ability #2"],
    },
    Spinda: {
      name: "Spinda",
      hp: 60,
      attack: 60,
      defense: 60,
      "special-attack": 60,
      "special-defense": 60,
      speed: 60,
      abilities: ["ability #1", "ability #2"],
    },
    Gengar: {
      name: "Gengar",
      hp: 60,
      attack: 60,
      defense: 50,
      "special-attack": 130,
      "special-defense": 90,
      speed: 110,
      abilities: ["ability #1", "ability #2"],
    },
  };

  const PkmnCard = styled(Card)({
    display: "flex",
    borderRadius: "30px",
    color: "var(--text)",
    boxShadow: "3px 3px 8px var(--box-shadow)",
  });

  return (
    <>
      <ul>
        {Object.values(pkmnTeam).map((pkmn) => (
          <PkmnCard
            key={pkmn.name.toLowerCase()}
            sx={{
              fontSize: "1rem",
              margin: "45px",
              border: 1,
              borderStyle: "solid",
              borderColor: "var(--text)",
            }}
          >
            <CardMedia
              component="img"
              sx={{ width: "128px", height: "128px", objectFit: "contain" }}
              image={`/pokemon_sprites/${pkmn.name.toLowerCase()}-sprite.png`}
              alt={pkmn.name + " sprite"}
            />
            <CardContent>
              <Typography component="div" variant="h5">
                {pkmn.name}
              </Typography>

              <Box
                sx={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "space-between",
                }}
              >
                <Typography component="div">
                  HP: {pkmn.hp} Attack: {pkmn.attack} Def: {pkmn.defense}
                </Typography>
                <Typography component="div">
                  Sp. Atk: {pkmn["special-attack"]} Sp. Def:
                  {pkmn["special-defense"]} Speed: {pkmn.speed}
                </Typography>
              </Box>
            </CardContent>
          </PkmnCard>
        ))}
      </ul>
    </>
  );
}
