import "../App.css";
import Button from "@mui/material/Button";

export default function GenerationSelect() {
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

  return (
    <>
      <ul>
        {gens.map((gen) => (
          <Button
            className={"rounded-rectangle button"}
            style={{
              background: "linear-gradient(45deg, #304fa3, #892A3A)",
              width: "248px",
              height: "128px",
              borderRadius: "30px",
              color: "#FFFFFF",
            }}
            sx={{ fontSize: "1rem", margin: "45px" }}
          >
            {gen}
          </Button>
        ))}
      </ul>
    </>
  );
}
