import "./AccountAccess.css";
import { Box, FormControl, TextField, Typography } from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../../context/AuthContext.tsx";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { setAuth } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();

  const userRef = useRef<HTMLInputElement>(null);
  const errRef = useRef<HTMLInputElement>(null);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    userRef.current?.focus();
  }, []);

  useEffect(() => {
    setErrorMsg("");
  }, [username, password]);

  async function logIn(event: { preventDefault: () => void }) {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (!response.ok) {
        if (response.status === 400) {
          setErrorMsg("Username or password missing");
        } else if (response.status === 401) {
          setErrorMsg("Unauthorized");
        } else {
          setErrorMsg("Login failed");
        }
        errRef.current?.focus();
        return;
      }

      const data = await response.json();
      // console.log(data);
      const { accessToken, user } = data;

      setAuth({
        accessToken,
        user: {
          account_id: user.account_id,
          username: user.username,
        },
      });

      setUsername("");
      setPassword("");

      // redirect to home page after logging in
      navigate("/");
    } catch (error: unknown) {
      setErrorMsg("No server response");
      errRef.current?.focus();
    }
  }

  return (
    <>
      <div className={"page-container"}>
        <Card
          className="account-card"
          sx={{
            background: "var(--rgba-gradient)",
            minHeight: "80vh",
            marginBottom: "15vh",
            borderRadius: "30px",
          }}
        >
          <CardContent
            component={"form"}
            sx={{ width: "80%vw", height: "80%vh" }}
            onSubmit={logIn}
          >
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

            {/* Error Message */}
            <Typography
              ref={errRef}
              className={errorMsg ? "errormsg" : "offscreen"}
            >
              {errorMsg}
            </Typography>

            <FormControl>
              <Box
                display={"flex"}
                flexDirection={"column"}
                alignItems={"center"}
              >
                {/* Username field */}
                <TextField
                  required
                  id="username"
                  type="text"
                  label="Username"
                  ref={userRef}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="off"
                  sx={{
                    width: "80%",
                    margin: "30px 50px 30px 50px",
                    fieldset: { borderColor: "var(--primary)" },
                    flexShrink: 0,
                  }}
                />

                {/* Password field */}
                <TextField
                  required
                  id="outlined-password-input"
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  sx={{
                    width: "80%",
                    margin: "30px 50px 30px 50px",
                    fieldset: { borderColor: "var(--primary)" },
                    flexShrink: 0,
                  }}
                />
              </Box>
              <Button
                type="submit"
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
            </FormControl>

            <div className={"dividing-line"}></div>

            <Typography>
              Don't have an account? {""}{" "}
              <Link
                className={"link-style"}
                to={"/register"}
                state={{ from: location.pathname }}
              >
                Register
              </Link>{" "}
              an account instead!
            </Typography>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
