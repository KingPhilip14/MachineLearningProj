import { Link, useLocation } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { mascot, mascot_shiny } from "../../assets";
import { Toggle } from "../toggle/Toggle.tsx";

// @ts-ignore
export default function Header({ isDark, setIsDark }) {
  const location = useLocation();

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
            src={isDark ? mascot_shiny : mascot}
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
        <Link className={"header-link"} to={"/login"}>
          <Button color="inherit">Login</Button>
        </Link>
        <Link
          className={"header-link"}
          to={"/register"}
          state={{ from: location.pathname }}
        >
          <Button color="inherit">Register</Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
}
