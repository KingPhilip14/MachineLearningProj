import "../../App.css";
import "./Home.css";
import Typography from "@mui/material/Typography";
import GenSelect from "../gen-selection/GenSelect.tsx";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import LinearGradText from "../LinearGradText.tsx";

export default function Home() {
  return (
    <>
      <div className={"page-container home"}>
        <Card
          className={"text-card"}
          style={{
            height: "140px",
            justifyContent: "center",
            borderRadius: "30px",
            background: "var(--tertiary)",
          }}
        >
          <CardContent>
            <Typography
              variant="h5"
              style={{ textAlign: "center", margin: 0, lineHeight: 1.4 }}
            >
              Welcome to PAIGE:
              <br />
              The Pokémon AI Generation Engine
            </Typography>
          </CardContent>
        </Card>
        <Typography className="text">
          Select a generation below to get started!
        </Typography>

        <LinearGradText text={"Generations"} />

        <div className={"rectangle-wrapper"}>
          <GenSelect />
        </div>
      </div>
    </>
  );
}
