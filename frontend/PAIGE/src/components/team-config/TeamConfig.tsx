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
  const [usingLittleCup, setUsingLittleCup] = React.useState(false);
  const [usingLegends, setUsingLegends] = React.useState(false);
  const [teamComp, setTeamComp] = React.useState("balanced");
  // const [littleCupLabel, setlittleCupLabel] = React.useState("no");

  const handleChange = (event: React.ChangeEvent) => {
    setUsingLittleCup(event.target.value);
  };

  const ConfigRadio = styled(Radio)({
    color: "var(--primary)",
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
                style={{ color: "var(--text)" }}
              >
                (Only baby Pokémon will be used)
              </FormLabel>
              <RadioGroup
                row
                name="position"
                defaultValue="top"
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
                style={{ color: "var(--text)" }}
              >
                (Legendaries <em>may</em> be generated but are not guaranteed)
              </FormLabel>
              <RadioGroup
                row
                name="position"
                defaultValue="top"
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
                style={{ color: "var(--text)" }}
              >
                (Affects the Pokémon considered for team generation)
              </FormLabel>
              <RadioGroup
                row
                name="position"
                defaultValue="top"
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
      </div>
    </>
  );
}
