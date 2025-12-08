import "./AccountAccess.css";
import { FormControl, TextField, Typography } from "@mui/material";
import { Link, useNavigate, useLocation } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useState } from "react";
// import { useState, useContext } from "react";
// import AuthContext from "../../context/AuthProvider.tsx";
// import axios from "./../../api/axios.tsx";
// const LOGIN_URL = "/auth";

export default function Register() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  // const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  // const { setAuth } = useContext(AuthContext);
  // const userRef = useRef("");
  // const errRef = useRef("");

  // useEffect(() => {
  //   userRef.current.focus();
  // }, []);

  // useEffect(() => {
  //   setMessage("");
  // }, [username, password]);

  async function registerUser(event: { preventDefault: () => void }) {
    // prevent a full page reload
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to register a new account");
      }

      // take the user to the last page they were on after successful registration
      navigate("/", { replace: true });
    } catch (error) {
      console.error(error);
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
            style={{ width: "80%vw", height: "80%vh" }}
            onSubmit={registerUser}
          >
            <Typography
              variant={"h3"}
              sx={{
                textAlign: "center",
                color: "var(--text)",
                margin: "40px 20px 20px 20px",
              }}
            >
              Register
            </Typography>
            <Typography variant="h6" style={{ margin: "40px 20px 40px 20px" }}>
              Create an account to save teams and access them!
            </Typography>

            <Typography>{message}</Typography>

            <FormControl>
              <div>
                <TextField
                  required
                  component={"div"}
                  id="username"
                  label="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{ margin: "30px 50px 30px 50px" }}
                  sx={{
                    fieldset: { borderColor: "var(--primary)" },
                  }}
                />
              </div>
              <div>
                <TextField
                  required
                  component={"div"}
                  id="outlined-password-input"
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ margin: "30px 50px 30px 50px" }}
                  sx={{
                    fieldset: { borderColor: "var(--primary)" },
                  }}
                />
              </div>
              {/*<div>*/}
              {/*  <TextField*/}
              {/*    required*/}
              {/*    id="outlined-password-input"*/}
              {/*    label="Confirm Password"*/}
              {/*    type="password"*/}
              {/*    value={confirmPassword}*/}
              {/*    onChange={(e) => setConfirmPassword(e.target.value)}*/}
              {/*    style={{ margin: "30px 50px 30px 50px" }}*/}
              {/*    sx={{*/}
              {/*      fieldset: { borderColor: "var(--primary)" },*/}
              {/*    }}*/}
              {/*  />*/}
              {/*</div>*/}
              <div>
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
                  Register
                </Button>
              </div>
            </FormControl>

            <div className={"dividing-line"}></div>

            <div>
              <Typography>
                Already have an account? {""}
                <Link className={"link-style"} to={"/login"}>
                  Log in
                </Link>{" "}
                to your account instead!
              </Typography>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
