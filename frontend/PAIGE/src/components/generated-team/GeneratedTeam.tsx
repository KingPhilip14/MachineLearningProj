import PokemonCard from "./PokemonCard.tsx";
import { SelectedGenCard } from "../SelectedGenCard.tsx";
import LinearGradText from "../LinearGradText.tsx";
import Button from "@mui/material/Button";
import { useLocation } from "react-router-dom";

export default function GeneratedTeam() {
  const location = useLocation();
  const { selectedGen } = location.state || {};

  return (
    <>
      <div className={"page-container"}>
        <SelectedGenCard selectedGen={selectedGen} backPage={"/team-config"} />
        <LinearGradText text={"Generated Team"} />

        <PokemonCard />

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
    </>
  );
}
