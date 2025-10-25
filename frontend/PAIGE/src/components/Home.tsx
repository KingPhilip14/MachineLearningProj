import "../App.css";
import Typography from "@mui/material/Typography";

export default function Home() {
  return (
    <div
      className={"rectangle"}
      style={{
        position: "absolute",
        top: "20%",
        left: "50%",
        transform: "translate(-50%, -50%)",
      }}
    >
      <Typography className="vert-hor-center-text" variant="h5">
        Welcome to PAIGE:
      </Typography>
      <Typography className="vert-hor-center-text" variant="h5">
        The Pokémon AI Generating Engine
      </Typography>
    </div>
  );
}
