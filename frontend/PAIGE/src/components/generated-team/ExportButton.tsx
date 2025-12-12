import Button from "@mui/material/Button";
import { capitalizeFirstLetter } from "./GeneratedTeamUtils.tsx";

interface Props {
  displayText: string;
  teamName: string;
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

const ExportButton = ({
  displayText,
  pkmnTeam,
  teamName = "My Team",
}: Props) => {
  const buildExport = (): string => {
    return Object.values(pkmnTeam || {})
      .map(
        (pkmn) =>
          `${pkmn.nickname} (${capitalizeFirstLetter(pkmn.name)}) 
          Ability: ${pkmn.chosen_ability} 
          Tera Type: ${capitalizeFirstLetter(pkmn.type_1)}
          `,
      )
      .join("\n");
  };

  const handleDownload = () => {
    const fileName = `${teamName}.txt`;
    const blob = new Blob([buildExport()], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);

    link.click();

    URL.revokeObjectURL(url);
    document.body.removeChild(link);
  };

  return (
    <Button
      variant={"contained"}
      size={"large"}
      sx={{
        backgroundColor: "var(--secondary)",
        color: "var(--text)",
        margin: "80px 0px 80px 0px",
        minHeight: "50px",
      }}
      onClick={handleDownload}
    >
      {displayText}
    </Button>
  );
};

export default ExportButton;
