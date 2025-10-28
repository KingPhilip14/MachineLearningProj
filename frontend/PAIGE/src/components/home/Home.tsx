import "../../App.css";
import Typography from "@mui/material/Typography";
import GenerationSelect from "../GenerationSelect.tsx";

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

        <div className={"rectangle-wrapper"}>
          <GenerationSelect />
        </div>
      </div>
    </>
  );
}
