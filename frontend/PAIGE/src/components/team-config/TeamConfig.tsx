import Card from "@mui/material/Card";
import LinearGradText from "../LinearGradText.tsx";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import {
  CardActions,
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Typography,
} from "@mui/material";
import { Link } from "react-router-dom";
import { styled } from "@mui/material/styles";
import React, { useState } from "react";

export default function TeamConfig() {
  const [usingLittleCup, setUsingLittleCup] = useState("no");
  const [disabledLegends, setDisabledLegends] = useState(false);
  const [legendsValue, setLegendsValue] = useState("no");

  // const handleChange = (event: React.ChangeEvent) => {
  //   console.log("Using Little Cup BEFORE change:", usingLittleCup);
  //   console.log("Legends disabled BEFORE change:", disabledLegends);
  //   console.log("Legends value BEFORE change:", legendsValue);
  //
  //   debugger;
  //   setUsingLittleCup(event.target.value);
  //   setDisabledLegends(usingLittleCup !== "yes");
  //   usingLittleCup === "yes" ? setLegendsValue("no") : setLegendsValue("yes");
  //
  //   console.log("Using Little Cup after change:", usingLittleCup);
  //   console.log("Legends disabled after change:", disabledLegends);
  //   console.log("Legends value after change:", legendsValue);
  // };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newLCValue = event.target.value;

    setUsingLittleCup(newLCValue);

    if (newLCValue === "yes") {
      setDisabledLegends(true);
      setLegendsValue("no");
    } else {
      setDisabledLegends(false);
    }
  };

  const ConfigRadio = styled(Radio)({
    color: "var(--primary)",
    transition: "color 150ms ease-in-out",
    "&.Mui-checked": {
      color: "var(--primary)",
    },
  });

  const ConfigCard = styled(Card)({
    height: "160px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: "30px",
    background: "var(--tertiary)",
  });

  return (
    <>
      <div className={"page-container"}>
        <ConfigCard className={"text-card"} style={{ flexDirection: "column" }}>
          <CardContent>
            <Typography
              variant="h5"
              style={{ textAlign: "center", margin: 0, lineHeight: 1.4 }}
            >
              Selected generation: [generation #]
            </Typography>
          </CardContent>
          <CardActions>
            <Link to={"/"}>
              <Button
                variant={"outlined"}
                size={"large"}
                sx={{ borderColor: "var(--text)", color: "var(--text)" }}
              >
                Back
              </Button>
            </Link>
          </CardActions>
        </ConfigCard>

        <Typography className="text">
          Configure your team preferences!
        </Typography>

        {/*Little Cup Configuration*/}
        <LinearGradText text={"Enable Little Cup?"} />

        <ConfigCard
          className={"text-card"}
          style={{ margin: "0px 0px 100px 0px" }}
        >
          <CardActions>
            <FormControl>
              <FormLabel
                id="demo-form-control-label-placement"
                style={{ color: "var(--text)", textAlign: "center" }}
              >
                (Only baby Pokémon will be used)
              </FormLabel>
              <RadioGroup
                row
                name="LC"
                value={usingLittleCup}
                // defaultValue="no"
                onChange={handleChange}
                style={{ justifyContent: "center", alignItems: "center" }}
              >
                <FormControlLabel
                  value="yes"
                  control={<ConfigRadio />}
                  label="Yes"
                  labelPlacement="bottom"
                  style={{ padding: "15px 35px 5px 10px" }}
                />
                <FormControlLabel
                  value="no"
                  control={<ConfigRadio />}
                  label="No"
                  labelPlacement="bottom"
                  style={{ padding: "15px 35px 5px 10px" }}
                />
              </RadioGroup>
            </FormControl>
          </CardActions>
        </ConfigCard>

        {/*Legendaries Configuration*/}
        <LinearGradText text={"Enable Legendaries?"} />

        <ConfigCard
          className={"text-card"}
          style={{ margin: "0px 0px 100px 0px" }}
        >
          <CardActions>
            <FormControl>
              <FormLabel
                id="demo-form-control-label-placement"
                style={{ color: "var(--text)", textAlign: "center" }}
              >
                (Legendaries <em>may</em> be generated but are not guaranteed)
              </FormLabel>
              <FormLabel style={{ color: "red", textAlign: "center" }}>
                (<em>Cannot</em> be used with Little Cup enabled)
              </FormLabel>
              <RadioGroup
                row
                name="legends"
                value={legendsValue}
                // defaultValue={"no"}
                onChange={(e) => setLegendsValue(e.target.value)}
                style={{ justifyContent: "center", alignItems: "center" }}
              >
                <FormControlLabel
                  value="yes"
                  control={<ConfigRadio />}
                  label="Yes"
                  labelPlacement="bottom"
                  disabled={disabledLegends}
                  style={{ padding: "15px 35px 5px 10px" }}
                />
                <FormControlLabel
                  value="no"
                  control={<ConfigRadio />}
                  label="No"
                  labelPlacement="bottom"
                  disabled={disabledLegends}
                  style={{ padding: "15px 35px 5px 10px" }}
                />
              </RadioGroup>
            </FormControl>
          </CardActions>
        </ConfigCard>

        {/*Team Composition Configuration*/}
        <LinearGradText text={"Which Team Composition?"} />

        <ConfigCard
          className={"text-card"}
          style={{ margin: "0px 0px 100px 0px" }}
        >
          <CardActions>
            <FormControl>
              <FormLabel
                id="demo-form-control-label-placement"
                style={{ color: "var(--text)", textAlign: "center" }}
              >
                (Affects the Pokémon considered for team generation)
              </FormLabel>
              <RadioGroup
                row
                name="team-composition"
                // defaultValue="balanced"
                style={{ justifyContent: "center", alignItems: "center" }}
              >
                <FormControlLabel
                  value="offensive"
                  control={<ConfigRadio />}
                  label="Offensive"
                  labelPlacement="bottom"
                  style={{ padding: "15px 35px 5px 10px" }}
                />
                <FormControlLabel
                  value="balanced"
                  control={<ConfigRadio />}
                  label="Balanced"
                  labelPlacement="bottom"
                  style={{ padding: "15px 35px 5px 10px" }}
                />
                <FormControlLabel
                  value="defensive"
                  control={<ConfigRadio />}
                  label="Defensive"
                  labelPlacement="bottom"
                  style={{ padding: "15px 35px 5px 10px" }}
                />
              </RadioGroup>
            </FormControl>
          </CardActions>
        </ConfigCard>

        {/* Generate button */}
        <Link to={"/generated-team"}>
          <Button
            variant={"contained"}
            size={"large"}
            sx={{
              backgroundColor: "var(--secondary)",
              color: "var(--text)",
              margin: "0px 0px 80px 0px",
              minHeight: "50px",
            }}
          >
            Generate Team
          </Button>
        </Link>
      </div>
    </>
  );
}
