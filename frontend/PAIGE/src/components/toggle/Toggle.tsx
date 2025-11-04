import "./Toggle.css";
import { InputLabel } from "@mui/material";

interface Props {
  handleChange: () => void;
  isChecked: boolean;
}

export const Toggle = ({ handleChange, isChecked }: Props) => {
  return (
    <div className="toggle-container">
      <input
        type={"checkbox"}
        id={"check"}
        className={"toggle"}
        onChange={handleChange}
        checked={isChecked}
      />
      <InputLabel htmlFor={"check"}>Dark Mode</InputLabel>
    </div>
  );
};

export default Toggle;
