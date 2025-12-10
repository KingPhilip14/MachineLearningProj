import "./AccountAccess.css";
import { Box, FormControl, TextField, Typography } from "@mui/material";
import {
  faCheck,
  faTimes,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link, useNavigate, useLocation } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import { useEffect, useRef, useState } from "react";

import React from "react";

const USER_REGEX = /^[A-z][A-z0-9-_]{3,29}$/;
const PASSWORD_REGEX = /^.{4,29}$/;

const NewRegister = () => {
  const userRef = useRef<HTMLInputElement>(null);
  const errRef = useRef<HTMLInputElement>(null);

  const [username, setUsername] = useState("");
  const [validName, setValidName] = useState(false);
  const [usernameFocus, setUsernameFocus] = useState(false);

  const [password, setPassword] = useState("");
  const [validPassword, setValidPassword] = useState(false);
  const [passwordFocus, setPasswordFocus] = useState(false);

  const [matchPassword, setMatchPassword] = useState("");
  const [validMatch, setValidMatch] = useState(false);
  const [matchFocus, setMatchFocus] = useState(false);

  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    userRef.current?.focus();
  }, []);

  useEffect(() => {
    const result = USER_REGEX.test(username);
    setValidName(result);
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

  return (
    <>
      <div className={"page-container"}>
        <section>
          <Typography
            ref={errRef}
            className={errorMsg ? "errormsg" : "offscreen"}
            sx={{ color: "red" }}
          >
            {errorMsg}
          </Typography>
        </section>

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
                  aria-invalid={validName ? "false" : "true"}
                  aria-describedby="uidnote"
                  onFocus={() => setUsernameFocus(true)}
                  onBlur={() => setUsernameFocus(false)}
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
                    className={validName ? "valid" : "hide"}
                  />
                  <FontAwesomeIcon
                    icon={faTimes}
                    className={validName || !username ? "hide" : "invalid"}
                  />
                </Box>
              </Box>
              <Typography
                id={"uidnote"}
                variant={"subtitle2"}
                sx={{ color: "text.secondary", marginBottom: "60px" }}
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
                  onFocus={() => setPasswordFocus(true)}
                  onBlur={() => setPasswordFocus(false)}
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
                sx={{ color: "text.secondary", marginBottom: "60px" }}
              >
                Passwords must be between 4-30 characters.
              </Typography>

              {/* Confirm password field */}
            </FormControl>
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default NewRegister;
