import "./AccountAccess.css";
import { TextField, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

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
              sx={{
                textAlign: "center",
                color: "var(--text)",
                margin: "40px 20px 20px 20px",
              }}
            >
              Login
            </Typography>
            <Typography variant="h6" style={{ margin: "40px 20px 40px 20px" }}>
              Log in to PAIGE to access your saved teams!
            </Typography>

            <TextField
              required
              id="username"
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ margin: "30px 50px 30px 50px" }}
              sx={{
                fieldset: { borderColor: "var(--primary)" },
              }}
            />
            <TextField
              required
              id="outlined-password-input"
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              style={{ margin: "30px 50px 30px 50px" }}
              sx={{
                fieldset: { borderColor: "var(--primary)" },
              }}
            />
            <div>
              <Button
                variant={"outlined"}
                size={"large"}
                sx={{
                  borderColor: "var(--primary)",
                  color: "var(--text)",
                  margin: "40px 30px 40px 30px",
                  padding: "15px 30px 15px 30px",
                }}
              >
                Log in
              </Button>
            </div>

            <div className={"dividing-line"}></div>

            <div>
              <Typography>
                Don't have an account? {""}{" "}
                <Link className={"link-style"} to={"/register"}>
                  Register
                </Link>{" "}
                an account instead!
              </Typography>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
