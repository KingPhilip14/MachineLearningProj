import "../../App.css";
import "./Home.css";
import Typography from "@mui/material/Typography";
import GenSelect from "../gen-selection/GenSelect.tsx";
import { LinearGradient } from "react-text-gradients";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";

export default function Home() {
  return (
    <>
      <div className={"home-page-container"}>
        <Card
          className={"text-card"}
          style={{
            width: "864px",
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

        <h3>
          <LinearGradient
            gradient={["to left", "var(--secondary), var(--primary)"]}
            fallbackColor="var(--text)"
          >
            Generations
          </LinearGradient>
        </h3>

        <div className={"rectangle-wrapper"}>
          <GenSelect />
        </div>
      </div>
    </>
  );
}
