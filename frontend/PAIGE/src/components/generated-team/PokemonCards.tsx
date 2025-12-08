import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import EditableTypography from "../EditableTypography.tsx";

export default function PokemonCards() {
  const pkmnTeam = {
    solrock: {
      name: "solrock",
      nickname: "Solrock",
      role: "Bulky",
      role_description:
        "Provides a general form of tankiness without having high defenses thanks to its high HP.",
      type_1: "rock",
      type_2: "psychic",
      hp: 90,
      attack: 95,
      defense: 85,
      special_attack: 65,
      special_defense: 65,
      speed: 70,
      bst: 460,
      abilities: ["Levitate"],
    },
    excadrill: {
      name: "excadrill",
      nickname: "Excadrill",
      role: "Physical Sweeper",
      role_description:
        "A fast, hard-hitting attacker that uses their astounding physical damage.",
      type_1: "ground",
      type_2: "steel",
      hp: 110,
      attack: 135,
      defense: 60,
      special_attack: 65,
      special_defense: 65,
      speed: 88,
      bst: 508,
      abilities: ["Sand Rush", "Sand Force", "Mold Breaker"],
    },
    jynx: {
      name: "jynx",
      nickname: "Jynx",
      role: "Special Sweeper",
      role_description:
        "An attacker excelling in special damage and speed to overwhelm the opponent.",
      type_1: "ice",
      type_2: "psychic",
      hp: 65,
      attack: 50,
      defense: 35,
      special_attack: 95,
      special_defense: 95,
      speed: 95,
      bst: 455,
      abilities: ["Oblivious", "Forewarn", "Dry Skin"],
    },
    seaking: {
      name: "seaking",
      nickname: "Seaking",
      role: "Versatile",
      role_description:
        "A flexible role that provides relatively balanced stats and can have unpredictable usage.",
      type_1: "water",
      type_2: "",
      hp: 80,
      attack: 92,
      defense: 65,
      special_attack: 80,
      special_defense: 80,
      speed: 68,
      bst: 450,
      abilities: ["Swift Swim", "Water Veil", "Lightning Rod"],
    },
    mantine: {
      name: "mantine",
      nickname: "Mantine",
      role: "Special Wall",
      role_description:
        "Absorbs special attacks, walling out special attackers. Both HP and Special Defense are notably high.",
      type_1: "water",
      type_2: "flying",
      hp: 85,
      attack: 40,
      defense: 70,
      special_attack: 140,
      special_defense: 140,
      speed: 70,
      bst: 485,
      abilities: ["Swift Swim", "Water Absorb", "Water Veil"],
    },
    miltank: {
      name: "miltank",
      nickname: "Miltank",
      role: "Physical Wall",
      role_description:
        "Eats physical hits without taking much of a scratch. Both HP and Defense are notably high.",
      type_1: "normal",
      type_2: "",
      hp: 95,
      attack: 80,
      defense: 105,
      special_attack: 70,
      special_defense: 70,
      speed: 100,
      bst: 490,
      abilities: ["Thick Fat", "Scrappy", "Sap Sipper"],
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
                      <EditableTypography
                        givenText={pkmn.nickname}
                        component="div"
                        variant="h5"
                        sx={{ marginRight: "5px" }}
                      />
                      {Types(pkmn.type_1, pkmn.type_2)}
                    </Box>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      Role: {pkmn.role}
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      BST: {pkmn.bst}
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
