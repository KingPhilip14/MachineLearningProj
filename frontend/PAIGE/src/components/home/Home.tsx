import "../../App.css";
import "./Home.css";
import Typography from "@mui/material/Typography";
import GenerationSelect from "../GenerationSelect.tsx";
import { LinearGradient } from "react-text-gradients";

export default function Home() {
  return (
    <>
      <div className={"home-page-container"}>
        <div
          className={"rounded-rectangle"}
          style={{ width: "864px", height: "140px" }}
        >
          <Typography
            variant="h5"
            style={{ textAlign: "center", margin: 0, lineHeight: 1.4 }}
          >
            Welcome to PAIGE:
            <br />
            The Pokémon AI Generation Engine
          </Typography>
        </div>
        <Typography style={{ padding: "75px", textAlign: "center" }}>
          Select a generation below to get started!
        </Typography>

        <h3>
          <LinearGradient
            gradient={["to left", "var(--light-primary), var(--dark-primary)"]}
            fallbackColor="var(--text)"
          >
            Generations
          </LinearGradient>
        </h3>

        <div className={"rectangle-wrapper"}>
          <GenerationSelect />
        </div>
      </div>
    </>
  );
}
