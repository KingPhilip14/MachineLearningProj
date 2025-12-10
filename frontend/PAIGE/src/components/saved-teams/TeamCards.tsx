import {
  Box,
  Card,
  CardMedia,
  CardContent,
  Typography,
  IconButton,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import DeleteIcon from "@mui/icons-material/Delete";
import ExportButton from "../generated-team/ExportButton.tsx";
import CopyButton from "../generated-team/CopyButton.tsx";
import type { Team } from "./SavedTeams.tsx";

interface TeamCardsProps {
  teams: Team[];
  accountId: number;
  onDeleteTeam: (teamId: number) => void;
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

interface PkmnTeam {
  [pokemonName: string]: PkmnEntry;
}

function convertToPkmnTeam(team: Team): PkmnTeam {
  const pkmnTeam: PkmnTeam = {};
  team.pokemon.forEach((p) => {
    pkmnTeam[p.pokemon_name.toLowerCase()] = {
      name: p.pokemon_name.toLowerCase(),
      nickname: p.nickname,
      type_1: "",
      type_2: "",
      hp: 0,
      attack: 0,
      defense: 0,
      special_attack: 0,
      special_defense: 0,
      speed: 0,
      bst: 0,
      role: "",
      role_description: "",
      chosen_ability: "",
      abilities: [],
    };
  });
  return pkmnTeam;
}

export const TeamCards = ({
  teams,
  accountId,
  onDeleteTeam,
}: TeamCardsProps) => {
  const TeamCard = styled(Card)({
    display: "flex",
    flexDirection: "column",
    borderRadius: "30px",
    color: "var(--text)",
    boxShadow: "3px 3px 8px var(--box-shadow)",
    width: "50vw",
    marginBottom: "2rem",
  });

  async function deleteTeam(teamId: number) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/account/${accountId}/delete-team/${teamId}`,
        {
          method: "DELETE",
        },
      );
      if (!response.ok) throw new Error("Failed to delete team");
      onDeleteTeam(teamId);
    } catch (err) {
      console.error(err);
      alert("Could not delete the team. Please try again.");
    }
  }

  return (
    <Box display="flex" flexDirection="column" alignItems="center" gap={4}>
      {teams.map((team) => (
        <TeamCard key={team.team_id}>
          <CardContent>
            <Typography variant="h6" mb={2}>
              {team.team_name}
            </Typography>
            <Box display="flex" justifyContent="space-around" mb={1}>
              {team.pokemon.map((p) => (
                <CardMedia
                  key={p.pit_id}
                  component="img"
                  image={`/pokemon_sprites/${p.pokemon_name.toLowerCase()}-sprite.png`}
                  alt={p.pokemon_name + " sprite"}
                  sx={{ width: 70, height: 70 }}
                />
              ))}
            </Box>
          </CardContent>

          {/* Bottom tray */}
          <Box
            display="flex"
            justifyContent="space-around"
            alignItems="center"
            borderTop="1px solid var(--text)"
            sx={{ m: 0, p: 0 }}
          >
            <ExportButton
              displayText="Export Team"
              teamName={team.team_name}
              pkmnTeam={convertToPkmnTeam(team)}
            />
            <CopyButton
              displayText="Copy Team"
              pkmnTeam={convertToPkmnTeam(team)}
            />
            <IconButton
              color="error"
              onClick={() => deleteTeam(team.team_id)}
              size="large"
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Box>
        </TeamCard>
      ))}
    </Box>
  );
};
