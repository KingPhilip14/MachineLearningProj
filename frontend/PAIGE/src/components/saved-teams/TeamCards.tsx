import { Box, Card, Typography } from "@mui/material";
import { styled } from "@mui/material/styles";

interface PokemonInTeam {
  pit_id: number;
  pokemon_id: number;
  pokemon_name: string;
  chosen_ability_id: number;
  nickname: string;
}

interface Team {
  team_id: number;
  team_name: string;
  pokemon: PokemonInTeam[];
}

interface TeamCardsProps {
  teams: Team[];
}

export const TeamCards = ({ teams }: TeamCardsProps) => {
  const TeamCard = styled(Card)({
    display: "flex",
    flexDirection: "column",
    borderRadius: "25px",
    color: "var(--text)",
    boxShadow: "5px 5px 15px var(--box-shadow)",
    padding: "2rem",
    width: "500px",
    minHeight: "250px",
    marginBottom: "2rem",
    alignItems: "center",
  });

  return (
    <Box display="flex" flexDirection="column" alignItems="center" width="100%">
      {teams.map((team) => (
        <TeamCard key={team.team_id}>
          <Typography variant="h5" mb={3} align="center">
            {team.team_name}
          </Typography>
          <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap">
            {team.pokemon.map((pkmn) => (
              <img
                key={pkmn.pit_id}
                src={`/pokemon_sprites/${pkmn.pokemon_name.toLowerCase()}-sprite.png`}
                alt={pkmn.pokemon_name}
                style={{ width: 100, height: 100 }}
              />
            ))}
          </Box>
        </TeamCard>
      ))}
    </Box>
  );
};
