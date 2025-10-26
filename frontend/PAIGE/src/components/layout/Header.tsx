import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import mascot from "../../assets/floette-eternal.gif";

export default function Header() {
  return (
    <AppBar
      style={{
        background: "linear-gradient(45deg, #304fa3, #892A3A)",
      }}
      sx={{ minHeight: "60px", position: "sticky" }}
    >
      <Toolbar>
        <img
          src={mascot}
          className="mascot"
          alt={"PAIGE Mascot"}
          // height="80px"
          style={{ padding: "15px" }}
        />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          PAIGE
        </Typography>
        <Button color="inherit">Login</Button>
        <Button color="inherit">About</Button>
        <Button color="inherit">Saved Teams</Button>
      </Toolbar>
    </AppBar>
  );
}
