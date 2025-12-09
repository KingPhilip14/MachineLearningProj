import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import EditableTypography from "../EditableTypography.tsx";
import AbilityMenu from "../AbilityMenu.tsx";

interface PokemonCardsProps {
  pkmnTeam: PkmnTeam; // the fetched team
  updateAbility: (name: string, ability: string) => void; // callback
}

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

export const PokemonCards = ({
  pkmnTeam,
  updateAbility,
}: PokemonCardsProps) => {
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
          {Object.values(pkmnTeam || {}).map((pkmn) => (
            <Grid size={{ xs: 6 }} key={pkmn.name?.toLowerCase()}>
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
};
