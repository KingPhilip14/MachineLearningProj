import { Link } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import mascot from "../../assets/floette-eternal.gif";
// import { Toggle } from "../toggle/Toggle.tsx";
// import { useState } from "react";

export default function Header() {
  // const [isDark, setIsDark] = useState(false);

  return (
    <AppBar
      style={{
        background: "var(--linear-gradient)",
      }}
      sx={{ minHeight: "60px", position: "sticky" }}
    >
      <Toolbar>
        <img
          src={mascot}
          className="mascot"
          alt={"PAIGE Mascot"}
          height="80px"
          style={{ padding: "15px" }}
        />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link className={"header-link"} to={"/"}>
            PAIGE
          </Link>
        </Typography>
        {/*<Toggle isChecked={isDark} handleChange={() => setIsDark(!isDark)} />*/}
        <Link className={"header-link"} to={"/about"}>
          <Button color="inherit">About</Button>
        </Link>
        <Button color="inherit">Saved Teams</Button>
        <Button color="inherit">Login</Button>
      </Toolbar>
    </AppBar>
  );
}
