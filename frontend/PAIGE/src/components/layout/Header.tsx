import { Link } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import mascot from "../../assets/floette-eternal.gif";
import { Toggle } from "../toggle/Toggle.tsx";

// @ts-ignore
export default function Header({ isDark, setIsDark }) {
  return (
    <AppBar
      style={{
        background: "var(--linear-gradient)",
      }}
      sx={{ position: "static" }}
    >
      <Toolbar>
        <Link to={"/about"}>
          <img
            src={mascot}
            className="mascot"
            alt={"PAIGE Mascot"}
            // height="80px"
            style={{ padding: "15px", position: "static" }}
          />
        </Link>

        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link className={"header-link"} to={"/"}>
            PAIGE
          </Link>
        </Typography>

        <Toggle isChecked={isDark} handleChange={() => setIsDark(!isDark)} />

        <Link className={"header-link"} to={"/about"}>
          <Button color="inherit">About</Button>
        </Link>
        <Button color="inherit">Saved Teams</Button>
        <Button color="inherit">Login</Button>
      </Toolbar>
    </AppBar>
  );
}
