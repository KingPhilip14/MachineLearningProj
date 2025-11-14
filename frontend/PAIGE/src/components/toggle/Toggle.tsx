import "./Toggle.css";
import { FormControlLabel, Switch } from "@mui/material";
// import { styled } from "@mui/material/styles";

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
      label="Dark Mode"
    />
  );
};

export default Toggle;
