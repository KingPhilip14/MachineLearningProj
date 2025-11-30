import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import { Box, CardMedia, Typography } from "@mui/material";
import Grid from "@mui/material/Grid";
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
      type_1: "psychic",
      type_2: "",
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
      type_1: "grass",
      type_2: "poison",
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
      type_1: "fire",
      type_2: "flying",
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
      type_1: "fighting",
      type_2: "",
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
      type_1: "normal",
      type_2: "",
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
      type_1: "ghost",
      type_2: "poison",
    },
  };

  const PkmnCard = styled(Card)({
    display: "flex",
    borderRadius: "30px",
    color: "var(--text)",
    boxShadow: "3px 3px 8px var(--box-shadow)",
  });

  function Types(type_1: string, type_2: string) {
    if (type_2 !== "") {
      return (
        <>
          <img src={`/types_sprites/${type_1}.png`} alt={`${type_1}`} />
          <img src={`/types_sprites/${type_2}.png`} alt={`${type_2}`} />
        </>
      );
    }

    return <img src={`/types_sprites/${type_1}.png`} alt={`${type_1}`} />;
  }

  return (
    <>
      <Grid container spacing={2} justifyContent={"center"}>
        {Object.values(pkmnTeam).map((pkmn) => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={pkmn.name.toLowerCase()}>
            <PkmnCard
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
                sx={{
                  width: "128px",
                  objectFit: "contain",
                  border: 1,
                  borderRadius: "30px",
                  borderColor: "var(--text)",
                  boxShadow: "1px 1px 5px var(--box-shadow)",
                }}
                image={`/pokemon_sprites/${pkmn.name.toLowerCase()}-sprite.png`}
                alt={pkmn.name + " sprite"}
              />
              <CardContent>
                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Typography sx={{ marginRight: "10px" }} variant="h5">
                    {pkmn.name}
                  </Typography>
                  {Types(pkmn.type_1, pkmn.type_2)}
                </Box>

                <Box
                  sx={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    rowGap: "5px",
                    columnGap: "15px",
                  }}
                >
                  {/*The order allows for it appear in the way desired*/}
                  <Typography>HP: {pkmn.hp}</Typography>
                  <Typography>Sp. Atk: {pkmn["special-attack"]}</Typography>
                  <Typography>Attack: {pkmn.attack}</Typography>
                  <Typography>Sp. Def: {pkmn["special-defense"]}</Typography>
                  <Typography>Def: {pkmn.defense}</Typography>
                  <Typography>Speed: {pkmn.speed}</Typography>
                </Box>
              </CardContent>
            </PkmnCard>
          </Grid>
        ))}
      </Grid>
    </>
  );
}
