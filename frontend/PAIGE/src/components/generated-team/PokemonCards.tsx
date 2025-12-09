import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import EditableTypography from "../EditableTypography.tsx";
import AbilityMenu from "../AbilityMenu.tsx";
import { useEffect, useState } from "react";
import { CircularProgress } from "@mui/material";

interface Props {
  selectedGen: string;
  usingLittleCup: string;
  usingLegends: string;
  composition: {
    more_offensive: boolean;
    more_defensive: boolean;
    more_balanced: boolean;
  };
}

export const PokemonCards = ({
  selectedGen,
  usingLittleCup,
  usingLegends,
  composition,
}: Props) => {
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

  const [pkmnTeam, setPkmnTeam] = useState<PkmnTeam>({});
  const [isLoading, setIsLoading] = useState(false);
  const [overlappingWeaknesses, setOverlappingWeaknesses] = useState<string[]>(
    [],
  );

  useEffect(() => {
    console.log("PokemonCards mounted");
    async function fetchTeam() {
      const data = await getGeneratedTeam();
      if (!data || !Array.isArray(data) || data.length === 0) return;

      setPkmnTeam(data[0]);

      if (data[1]?.overlapping_weaknesses) {
        setOverlappingWeaknesses(data[1].overlapping_weaknesses);
      }
    }

    fetchTeam();
  }, []);

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

  async function getGeneratedTeam() {
    const genFileName = selectedGen
      ? selectedGen.replace(" ", "_").toLowerCase()
      : "national";

    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/generate-team", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          using_little_cup: usingLittleCup,
          using_legends: usingLegends,
          gen_file_name: genFileName,
          composition: composition,
        }),
      });

      if (!response.ok) {
        throw new Error("A new team was not able to be generated.");
      }

      const data = await response.json();

      return data || {};
    } catch (error) {
      console.error(error);

      return {};
    } finally {
      setIsLoading(false);
    }
  }

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
      {isLoading ? (
        <div style={{ display: "flex", alignItems: "center", height: "50vh" }}>
          <CircularProgress size="10rem" sx={{ color: "var(--primary)" }} />
        </div>
      ) : (
        <Box display="flex" justifyContent="center" width="100%">
          <Grid
            container
            spacing={2}
            justifyContent="center"
            sx={{ maxWidth: "70rem", marginTop: "3rem" }}
          >
            {Object.values(pkmnTeam || {}).map((pkmn) => (
              <Grid
                size={{ xs: 6 }}
                key={pkmn.name?.toLowerCase() || Math.random()}
              >
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
                        onSelect={(ability) =>
                          updateAbility(pkmn.name, ability)
                        }
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
            {!isLoading && (
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                sx={{ mt: 5 }}
              >
                <Typography sx={{ mb: 2, textAlign: "center" }}>
                  This team has the following overlapping weaknesses. Be
                  mindful!
                </Typography>
                <Box
                  display="flex"
                  flexDirection="row"
                  justifyContent="center"
                  gap={3}
                >
                  {overlappingWeaknesses.map((weakness) => (
                    <img
                      key={weakness}
                      src={`/types_sprites/${weakness}.png`}
                      alt={weakness}
                    />
                  ))}
                </Box>
              </Box>
            )}
          </Grid>
        </Box>
      )}
    </>
  );
};
