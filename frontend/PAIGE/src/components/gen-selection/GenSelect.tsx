import "../../App.css";
import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";
import { Link } from "react-router-dom";

export default function GenSelect() {
  const gens = [
    "Gen 1",
    "Gen 2",
    "Gen 3",
    "Gen 4",
    "Gen 5",
    "Gen 6",
    "Gen 7",
    "Gen 8",
    "Gen 9",
    "National",
  ];

  const GenSelectBtn = styled(Button)({
    width: "248px",
    height: "128px",
    borderRadius: "30px",
    color: "var(--text)",
    boxShadow: "3px 3px 8px var(--box-shadow)",
  });

  return (
    <>
      <ul>
        {gens.map((gen) => (
          <Link to={"/team-config"} state={{ selectedGen: gen }} key={gen}>
            <GenSelectBtn
              sx={{
                fontSize: "1rem",
                margin: "45px",
                border: 1,
                borderStyle: "solid",
                borderColor: "var(--text)",
              }}
            >
              {gen}
            </GenSelectBtn>
          </Link>
        ))}
      </ul>
    </>
  );
}
