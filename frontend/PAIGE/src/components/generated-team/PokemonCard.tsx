import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";

export default function PokemonCard() {
  const pkmnTeam = {
    Abra: {
      name: "Abra",
      role: "Special Attacker",
      hp: 30,
      attack: 10,
      defense: 10,
      special_attack: 100,
      special_defense: 75,
      speed: 80,
      abilities: ["ability #1", "ability #2"],
      bst: 289,
      type_1: "psychic",
      type_2: "",
    },
    Bulbasaur: {
      name: "Bulbasaur",
      role: "Baby or sum",
      hp: 55,
      attack: 65,
      defense: 50,
      special_attack: 65,
      special_defense: 65,
      speed: 50,
      abilities: ["ability #1", "ability #2"],
      bst: 365,
      type_1: "grass",
      type_2: "poison",
    },
    Charizard: {
      name: "Charizard",
      role: "Special Attacker",
      hp: 80,
      attack: 90,
      defense: 80,
      special_attack: 102,
      special_defense: 85,
      bst: 525,
      speed: 80,
      abilities: ["ability #1", "ability #2"],
      type_1: "fire",
      type_2: "flying",
    },
    Machop: {
      name: "Machop",
      role: "Physical Attacker",
      hp: 65,
      attack: 80,
      defense: 64,
      special_attack: 30,
      special_defense: 45,
      bst: 325,
      speed: 60,
      abilities: ["ability #1", "ability #2"],
      type_1: "fighting",
      type_2: "",
    },
    Spinda: {
      name: "Spinda",
      role: "Versatile",
      hp: 60,
      attack: 60,
      defense: 60,
      special_attack: 60,
      special_defense: 60,
      speed: 60,
      bst: 360,
      abilities: ["ability #1", "ability #2"],
      type_1: "normal",
      type_2: "",
    },
    Gengar: {
      name: "Gengar",
      role: "Special Sweeper",
      hp: 60,
      attack: 60,
      defense: 50,
      special_attack: 130,
      special_defense: 90,
      speed: 110,
      bst: 510,
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
        <div>
          <img src={`/types_sprites/${type_1}.png`} alt={`${type_1}`} />
          <img src={`/types_sprites/${type_2}.png`} alt={`${type_2}`} />
        </div>
      );
    }

    return <img src={`/types_sprites/${type_1}.png`} alt={`${type_1}`} />;
  }

  return (
    <>
      <Box display="flex" justifyContent="center" width="100%">
        <Grid
          container
          spacing={2}
          justifyContent="center"
          sx={{ maxWidth: "70rem", marginTop: "3rem" }}
        >
          {Object.values(pkmnTeam).map((pkmn) => (
            <Grid size={{ xs: 6 }} key={pkmn.name.toLowerCase()}>
              <PkmnCard
                sx={{
                  // display: "flex",
                  // margin: "45px",
                  // border: 1,
                  // borderStyle: "solid",
                  // borderColor: "var(--text)",
                  // minWidth: "50%",
                  // maxWidth: "80%",
                  // minHeight: "75%",

                  display: "flex",
                  border: 1,
                  borderStyle: "solid",
                  borderColor: "var(--text)",
                  width: "100%",
                  height: "100%",
                  p: 2,
                }}
              >
                <CardMedia
                  className="sprite"
                  component="img"
                  sx={{
                    width: 151,
                    objectFit: "contain",
                  }}
                  image={`/pokemon_sprites/${pkmn.name.toLowerCase()}-sprite.png`}
                  alt={pkmn.name + " sprite"}
                />
                <Box sx={{ display: "flex", flexDirection: "column" }}>
                  <CardContent sx={{ flex: "1 0 auto" }}>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                      <Typography
                        component="div"
                        variant="h5"
                        sx={{ marginRight: "5px" }}
                      >
                        {pkmn.name}
                      </Typography>
                      {Types(pkmn.type_1, pkmn.type_2)}
                    </Box>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      {pkmn.role}
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      BST: 500
                    </Typography>
                  </CardContent>
                  <Box
                    sx={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr 1fr",
                      rowGap: "5px",
                      columnGap: "20px",
                      alignItems: "center",
                      pl: 1,
                      pb: 1,
                      margin: "5px",
                    }}
                  >
                    {/*The order allows for it appear in the way desired*/}
                    <Typography>
                      <b>HP</b>: {pkmn.hp}
                    </Typography>
                    <Typography>
                      <b>Attack</b>: {pkmn.attack}
                    </Typography>
                    <Typography>
                      <b>Def</b>: {pkmn.defense}
                    </Typography>
                    <Typography>
                      <b>Sp. Atk</b>: {pkmn.special_attack}
                    </Typography>
                    <Typography>
                      <b>Sp. Def</b>: {pkmn.special_defense}
                    </Typography>
                    <Typography>
                      <b>Speed</b>: {pkmn.speed}
                    </Typography>
                  </Box>
                </Box>
              </PkmnCard>
            </Grid>
          ))}
        </Grid>
      </Box>
    </>
  );
}
