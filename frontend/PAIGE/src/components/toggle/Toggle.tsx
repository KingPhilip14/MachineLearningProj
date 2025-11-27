import "./Toggle.css";
import { FormControlLabel, Switch, Typography } from "@mui/material";

interface Props {
  handleChange: () => void;
  isChecked: boolean;
}

export const Toggle = ({ handleChange, isChecked }: Props) => {
  return (
    <FormControlLabel
      control={
        <Switch
          defaultChecked
          color="default"
          checked={isChecked}
          onChange={handleChange}
        />
      }
      label={<Typography sx={{ fontSize: "14px" }}>DARK MODE</Typography>}
    />
  );
};

export default Toggle;
