import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";

export default function Header() {
  return (
    <AppBar
      position="sticky"
      style={{
        background: "linear-gradient(45deg, #1f271b, #0b4f6c)",
      }}
    >
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
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
