import PokemonCard from "./PokemonCard.tsx";
import { SelectedGenCard } from "../SelectedGenCard.tsx";
import LinearGradText from "../LinearGradText.tsx";
import Button from "@mui/material/Button";

export default function GeneratedTeam() {
  return (
    <>
      <div className={"page-container"}>
        <SelectedGenCard selectedGen={"Random gen"} backPage={"/team-config"} />
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
