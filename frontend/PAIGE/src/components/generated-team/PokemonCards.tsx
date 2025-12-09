import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import EditableTypography from "../EditableTypography.tsx";
import AbilityMenu from "../AbilityMenu.tsx";
import { useState } from "react";

export default function PokemonCards() {
  const initialTeamData = {
    sandaconda: {
      name: "sandaconda",
      nickname: "Sandaconda",
      role: "Physical Wall",
      role_description:
        "Eats physical hits without taking much of a scratch. Both HP and Defense are notably high.",
      type_1: "ground",
      type_2: "",
      hp: 72,
      attack: 107,
      defense: 125,
      special_attack: 70,
      special_defense: 70,
      speed: 71,
      bst: 510,
      chosen_ability: "Sand Spit",
      abilities: ["Sand Spit", "Shed Skin", "Sand Veil"],
    },
    garganacl: {
      name: "garganacl",
      nickname: "Garganacl",
      role: "Bulky",
      role_description:
        "Provides a general form of tankiness without having high defenses thanks to its high HP.",
      type_1: "rock",
      type_2: "",
      hp: 100,
      attack: 100,
      defense: 130,
      special_attack: 90,
      special_defense: 90,
      speed: 35,
      bst: 500,
      chosen_ability: "Purifying Salt",
      abilities: ["Purifying Salt", "Sturdy", "Clear Body"],
    },
    cryogonal: {
      name: "cryogonal",
      nickname: "Cryogonal",
      role: "Special Wall",
      role_description:
        "Absorbs special attacks, walling out special attackers. Both HP and Special Defense are notably high.",
      type_1: "ice",
      type_2: "",
      hp: 80,
      attack: 50,
      defense: 50,
      special_attack: 135,
      special_defense: 135,
      speed: 105,
      bst: 515,
      chosen_ability: "Levitate",
      abilities: ["Levitate"],
    },
    floette: {
      name: "floette",
      nickname: "Floette",
      role: "Eviolite User",
      role_description:
        "While not fully evolved, an Eviolite will make this PokÃ©mon as bulky as another Wall archetype, providing unique usage.",
      type_1: "fairy",
      type_2: "",
      hp: 54,
      attack: 45,
      defense: 47,
      special_attack: 98,
      special_defense: 98,
      speed: 52,
      bst: 371,
      chosen_ability: "Flower Veil",
      abilities: ["Flower Veil", "Symbiosis"],
    },
    "gallade-mega": {
      name: "gallade-mega",
      nickname: "Gallade-mega",
      role: "Physical Sweeper",
      role_description:
        "A fast, hard-hitting attacker that uses their astounding physical damage.",
      type_1: "psychic",
      type_2: "fighting",
      hp: 68,
      attack: 165,
      defense: 95,
      special_attack: 115,
      special_defense: 115,
      speed: 110,
      bst: 618,
      chosen_ability: "Inner Focus",
      abilities: ["Inner Focus"],
    },
    dusknoir: {
      name: "dusknoir",
      nickname: "Dusknoir",
      role: "Bulky Wall",
      role_description:
        "Can take both physical and special damage well. Both Defense and Special Defense are notably high, but HP may not be.",
      type_1: "ghost",
      type_2: "",
      hp: 45,
      attack: 100,
      defense: 135,
      special_attack: 135,
      special_defense: 135,
      speed: 45,
      bst: 525,
      chosen_ability: "Pressure",
      abilities: ["Pressure", "Frisk"],
    },
  };

  interface PkmnEntry {
    name: string;
    nickname: string;
    role: string;
    role_description: string;
    type_1: string;
    type_2: string;
    hp: number;
    attack: number;
    defense: number;
    special_attack: number;
    special_defense: number;
    speed: number;
    bst: number;
    chosen_ability: string;
    abilities: string[];
  }

  interface PkmnTeam {
    [pokemonName: string]: PkmnEntry;
  }

  const [pkmnTeam, setPkmnTeam] = useState<PkmnTeam>(initialTeamData);

  const PkmnCard = styled(Card)({
    display: "flex",
    borderRadius: "30px",
    color: "var(--text)",
    boxShadow: "3px 3px 8px var(--box-shadow)",
  });

  const updateAbility = (name: string, ability: string) => {
    setPkmnTeam((prev) => ({
      ...prev,
      [name]: {
        ...prev[name],
        chosen_ability: ability,
      },
    }));
  };

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
                      <em>
                        <b>Role</b>: {pkmn.role}
                      </em>
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      <em>
                        <b>Chosen Ability</b>: {pkmn.chosen_ability}
                      </em>
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      component="div"
                      sx={{ color: "text.secondary" }}
                    >
                      <em>
                        <b>BST</b>: {pkmn.bst}
                      </em>
                    </Typography>
                    <AbilityMenu
                      menuText={"Change Ability"}
                      pkmnName={pkmn.name}
                      abilities={pkmn.abilities}
                      onSelect={(ability) => updateAbility(pkmn.name, ability)}
                    />
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
