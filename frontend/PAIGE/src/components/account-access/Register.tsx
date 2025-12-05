import "./AccountAccess.css";
import { FormControl, TextField, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useState } from "react";
// import { useState, useContext } from "react";
// import AuthContext from "../../context/AuthProvider.tsx";
// import axios from "./../../api/axios.tsx";
// const LOGIN_URL = "/auth";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    // try {
    //   const response = await axios.post(
    //     LOGIN_URL,
    //     JSON.stringify({ username, password }),
    //     {
    //       headers: { "Content-Type": "application/json" },
    //       withCredentials: true,
    //     },
    //   );
    //   console.log(JSON.stringify(response?.data));
    //   setAuth(username, password);
    // }
    // catch (error) {
    //   if(!error?.response) {
    //     setMessage("No server response");
    //   }
    //   else if (error?.response?.status === 400) {
    //     setMessage("Missing username or password");
    //     }
    //   else if (error?.response?.status === 401) {
    //     setMessage("Unauthorized");
    //     }
    //   else {
    //     setMessage("Login failed");
    //     }
    //   }
    // }

    setMessage("Success!");

    // try {
    //   const response = await fetch("http://localhost:8000/register", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       username: username,
    //       password: password,
    //     }),
    //   });
    //
    //   if (response.ok) {
    //     const data = await response.json();
    //     setMessage(`Account registered successfully! ID: ${data.account_id}`);
    //   } else {
    //     const error = await response.json();
    //     setMessage(`Error: ${error.detail``}`);
    //   }
    // } catch (error) {
    //   setMessage("An error occurred while registering a new account.");
    // }
  };

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
            onSubmit={handleSubmit}
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
              <div>
                <TextField
                  required
                  id="outlined-password-input"
                  label="Confirm Password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  style={{ margin: "30px 50px 30px 50px" }}
                  sx={{
                    fieldset: { borderColor: "var(--primary)" },
                  }}
                />
              </div>
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
