import "./AccountAccess.css";
import { Box, FormControl, TextField, Typography } from "@mui/material";
import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link, useNavigate } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useEffect, useRef, useState } from "react";

const USER_REGEX = /^[A-z][A-z0-9-_]{3,29}$/;
const PASSWORD_REGEX = /^.{4,29}$/;

const Register = () => {
  const navigate = useNavigate();

  const userRef = useRef<HTMLInputElement>(null);
  const errRef = useRef<HTMLInputElement>(null);

  const [username, setUsername] = useState("");
  const [validUsername, setValidUsername] = useState(false);

  const [password, setPassword] = useState("");
  const [validPassword, setValidPassword] = useState(false);

  const [matchPassword, setMatchPassword] = useState("");
  const [validMatch, setValidMatch] = useState(false);

  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    userRef.current?.focus();
  }, []);

  useEffect(() => {
    const result = USER_REGEX.test(username);
    setValidUsername(result);
  }, [username]);

  useEffect(() => {
    const result = PASSWORD_REGEX.test(password);
    setValidPassword(result);

    const match = password === matchPassword;
    setValidMatch(match);
  }, [password, matchPassword]);

  useEffect(() => {
    setErrorMsg("");
  }, [username, password, matchPassword]);

  async function registerUser(event: { preventDefault: () => void }) {
    event.preventDefault();

    // used to help prevent attempts at maliciously enabling the button
    const testUsername = USER_REGEX.test(username);
    const testPassword = PASSWORD_REGEX.test(password);

    if (!testUsername || !testPassword) {
      setErrorMsg("Invalid entry");
      return;
    }

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

      if (response.ok) {
        // take the user to the home page
        navigate("/", { replace: true });
        return;
      }

      setErrorMsg("Could not register account. Try a different username");
    } catch (error: unknown) {
      if (error instanceof Error) {
        setErrorMsg("No server response");
      } else {
        setErrorMsg("Could not register account. Try a different username");
      }

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

            {/* Error message */}
            <Typography
              ref={errRef}
              className={errorMsg ? "errormsg" : "offscreen"}
            >
              {errorMsg}
            </Typography>

            <FormControl>
              {/* Username field */}
              <Box
                display={"flex"}
                flexDirection={"row"}
                alignItems={"center"}
                sx={{ width: "400px" }}
              >
                <TextField
                  required
                  component={"div"}
                  ref={userRef}
                  autoComplete="off"
                  type="text"
                  id="username"
                  label="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  aria-invalid={validUsername ? "false" : "true"}
                  aria-describedby="uidnote"
                  sx={{
                    margin: "30px 50px 30px 50px",
                    fieldset: { borderColor: "var(--primary)" },
                    width: "75%",
                    flexShrink: 0,
                  }}
                />
                <Box>
                  <FontAwesomeIcon
                    icon={faCheck}
                    className={validUsername ? "valid" : "hide"}
                  />
                  <FontAwesomeIcon
                    icon={faTimes}
                    className={validUsername || !username ? "hide" : "invalid"}
                  />
                </Box>
              </Box>
              <Typography
                id={"uidnote"}
                variant={"subtitle2"}
                sx={{ color: "text.secondary", marginBottom: "30px" }}
              >
                Usernames must be between 4-30 characters and start with a
                letter.
              </Typography>

              {/* Password field */}
              <Box
                display={"flex"}
                flexDirection={"row"}
                alignItems={"center"}
                sx={{ width: "400px" }}
              >
                <TextField
                  required
                  component={"div"}
                  ref={userRef}
                  autoComplete="off"
                  type="password"
                  id="outlined-password-input"
                  label="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  aria-invalid={validPassword ? "false" : "true"}
                  aria-describedby="pwdnote"
                  sx={{
                    margin: "30px 50px 30px 50px",
                    fieldset: { borderColor: "var(--primary)" },
                    width: "75%",
                    flexShrink: 0,
                  }}
                />
                <Box>
                  <FontAwesomeIcon
                    icon={faCheck}
                    className={validPassword ? "valid" : "hide"}
                  />
                  <FontAwesomeIcon
                    icon={faTimes}
                    className={validPassword || !password ? "hide" : "invalid"}
                  />
                </Box>
              </Box>
              <Typography
                id={"uidnote"}
                variant={"subtitle2"}
                sx={{ color: "text.secondary", marginBottom: "30px" }}
              >
                Passwords must be between 4-30 characters.
              </Typography>

              {/* Confirm password field */}
              <Box
                display={"flex"}
                flexDirection={"row"}
                alignItems={"center"}
                sx={{ width: "400px" }}
              >
                <TextField
                  required
                  component={"div"}
                  ref={userRef}
                  autoComplete="off"
                  type="password"
                  id="confirm-password-input"
                  label="Confirm Password"
                  value={matchPassword}
                  onChange={(e) => setMatchPassword(e.target.value)}
                  aria-invalid={validPassword ? "false" : "true"}
                  aria-describedby="confirmnote"
                  sx={{
                    margin: "30px 50px 30px 50px",
                    fieldset: { borderColor: "var(--primary)" },
                    width: "75%",
                    flexShrink: 0,
                  }}
                />
                <Box>
                  <FontAwesomeIcon
                    icon={faCheck}
                    className={validMatch && matchPassword ? "valid" : "hide"}
                  />
                  <FontAwesomeIcon
                    icon={faTimes}
                    className={
                      validMatch || !matchPassword ? "hide" : "invalid"
                    }
                  />
                </Box>
              </Box>
              <Typography
                id={"uidnote"}
                variant={"subtitle2"}
                sx={{ color: "text.secondary", marginBottom: "30px" }}
              >
                The passwords must match.
              </Typography>

              <Button
                type="submit"
                variant={"outlined"}
                size={"large"}
                disabled={!validUsername || !validPassword || !validMatch}
                sx={{
                  borderColor: "var(--primary)",
                  color: "var(--text)",
                  margin: "40px 30px 40px 30px",
                  padding: "15px 30px 15px 30px",
                }}
              >
                Register
              </Button>
            </FormControl>

            <div className={"dividing-line"}></div>

            <div>
              <Typography sx={{ marginBottom: "60px" }}>
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
};

export default Register;
