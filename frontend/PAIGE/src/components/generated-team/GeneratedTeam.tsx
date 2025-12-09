import { PokemonCards } from "./PokemonCards.tsx";
import { SelectedGenCard } from "../SelectedGenCard.tsx";
import LinearGradText from "../LinearGradText.tsx";
import Button from "@mui/material/Button";
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { CircularProgress } from "@mui/material";

export default function GeneratedTeam() {
  interface PkmnTeam {
    [pokemonName: string]: PkmnEntry;
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

  const location = useLocation();
  const [pkmnTeam, setPkmnTeam] = useState<PkmnTeam>({});
  const [isLoading, setIsLoading] = useState(false);
  const [overlappingWeaknesses, setOverlappingWeaknesses] = useState<string[]>(
    [],
  );
  const { selectedGen, usingLittleCup, usingLegends, composition } =
    location.state || {};

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

  return (
    <>
      {isLoading ? (
        <div style={{ display: "flex", alignItems: "center", height: "50vh" }}>
          <CircularProgress size="10rem" sx={{ color: "var(--primary)" }} />
        </div>
      ) : (
        <div className={"page-container"}>
          <SelectedGenCard
            selectedGen={selectedGen}
            backPage={"/team-config"}
          />
          <LinearGradText text={"Generated Team"} />

          <PokemonCards
            pkmnTeam={pkmnTeam}
            updateAbility={(name, ability) =>
              setPkmnTeam((prev) => ({
                ...prev,
                [name]: { ...prev[name], chosen_ability: ability },
              }))
            }
          />

          {!isLoading && (
            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              sx={{ mt: 5 }}
            >
              <Typography sx={{ mb: 2, textAlign: "center" }}>
                This team has the following overlapping weaknesses. Be mindful!
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

          <Button
            variant={"contained"}
            size={"large"}
            sx={{
              backgroundColor: "var(--secondary)",
              color: "var(--text)",
              margin: "80px 0px 80px 0px",
              minHeight: "50px",
            }}
          >
            Save Team
          </Button>
        </div>
      )}
    </>
  );
}
