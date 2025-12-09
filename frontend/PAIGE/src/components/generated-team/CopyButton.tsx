import Button from "@mui/material/Button";
import { useState } from "react";

interface Props {
  displayText: string;
  pkmnTeam: PkmnTeam;
}

interface PkmnTeam {
  [pokemonName: string]: PkmnEntry;
}

interface PkmnEntry {
  name: string;
  nickname: string;
  role: string;
  role_description: string;
  type_1: string;
  type_2: string;
  hp: number;
  attack: number;
  defense: number;
  special_attack: number;
  special_defense: number;
  speed: number;
  bst: number;
  chosen_ability: string;
  abilities: string[];
}

const CopyButton = ({ displayText, pkmnTeam }: Props) => {
  const [copySuccessMsg, setCopySuccessMsg] = useState("");

  const buildExport = (): string => {
    return Object.values(pkmnTeam || {})
      .map(
        (pkmn) =>
          `${pkmn.nickname} (${pkmn.name}) 
          Ability: ${pkmn.chosen_ability} 
          Tera Type: ${pkmn.type_1}
          `,
      )
      .join("\n");
  };

  const handleCopyClick = async () => {
    try {
      await navigator.clipboard.writeText(buildExport());
      setCopySuccessMsg("Copied!");
    } catch (err) {
      setCopySuccessMsg("Failed to copy!");
      console.error("Failed to copy text: ", err);
    }

    setTimeout(() => setCopySuccessMsg(""), 2000);
  };

  return (
    <>
      <Button
        variant="contained"
        size="large"
        sx={{
          backgroundColor: "var(--secondary)",
          color: "var(--text)",
          margin: "80px 0px",
          minHeight: "50px",
        }}
        onClick={handleCopyClick}
      >
        {displayText}
      </Button>
    </>
  );
};

export default CopyButton;
