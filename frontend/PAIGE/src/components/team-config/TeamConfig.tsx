import Card from "@mui/material/Card";
import LinearGradText from "../LinearGradText.tsx";
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
import { Link, useLocation } from "react-router-dom";
import { styled } from "@mui/material/styles";
import React, { useState } from "react";
import { SelectedGenCard } from "../SelectedGenCard.tsx";

export default function TeamConfig() {
  const location = useLocation();
  const { selectedGen } = location.state || {};

  const [usingLittleCup, setUsingLittleCup] = useState("no");
  const [disabledLegends, setDisabledLegends] = useState(false);
  const [usingLegends, setUsingLegends] = useState("no");
  const [composition, setComposition] = useState("balanced");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newLCValue = event.target.value;

    setUsingLittleCup(newLCValue);

    if (newLCValue === "yes") {
      setDisabledLegends(true);
      setUsingLegends("no");
    } else {
      setDisabledLegends(false);
    }
  };

  const handleCompositionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setComposition(e.target.value);
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
        <SelectedGenCard selectedGen={selectedGen} backPage={"/"} />

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
                value={usingLegends}
                // defaultValue={"no"}
                onChange={(e) => setUsingLegends(e.target.value)}
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
                value={composition}
                onChange={handleCompositionChange}
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
        <Link
          to={"/generated-team"}
          state={{
            selectedGen: selectedGen,
            usingLittleCup: usingLittleCup === "yes",
            usingLegends: usingLegends === "yes",
            composition: composition,
          }}
        >
          <Button
            variant={"contained"}
            size={"large"}
            sx={{
              backgroundColor: "var(--secondary)",
              color: "var(--text)",
              marginBottom: "80px",
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
