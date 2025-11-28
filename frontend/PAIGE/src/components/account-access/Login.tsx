import "./AccountAccess.css";
import { TextField, Typography } from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";

export default function Login() {
  return (
    <>
      <div className={"page-container"}>
        <Card
          className="account-card"
          sx={{
            background: "var(--rgba-gradient)",
            minHeight: "80vh",
          }}
        >
          <CardContent style={{ width: "80%vw", height: "80%vh" }}>
            <Typography
              variant={"h3"}
              sx={{ textAlign: "center", color: "var(--text)" }}
            >
              Login
            </Typography>

            <TextField required id="username" label="Username" />
            <TextField
              required
              id="outlined-password-input"
              label="Password"
              type="password"
              autoComplete="current-password"
            />
          </CardContent>
        </Card>
      </div>
    </>
  );
}
