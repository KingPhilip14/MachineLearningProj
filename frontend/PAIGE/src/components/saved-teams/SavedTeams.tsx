import { useEffect, useState } from "react";
import { Box, CircularProgress, Typography } from "@mui/material";
import { useAuth } from "../../context/AuthContext.tsx";
import { TeamCards } from "./TeamCards.tsx";

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

interface AccountTeams {
  account_id: number;
  username: string;
  teams: Team[];
}

export default function SavedTeams() {
  const { auth } = useAuth();
  const [savedTeams, setSavedTeams] = useState<AccountTeams | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!auth.user) return;
    fetchSavedTeams(auth.user.account_id);
  }, [auth.user]);

  async function fetchSavedTeams(accountId: number) {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/account/${accountId}/saved-teams`,
      );
      if (!response.ok) throw new Error("Failed to fetch saved teams");
      const data = await response.json();
      setSavedTeams(data[0] || null);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100vh"
      >
        <CircularProgress size="5rem" sx={{ color: "var(--primary)" }} />
      </Box>
    );
  }

  if (!savedTeams || savedTeams.teams.length === 0) {
    return (
      <Box display="flex" justifyContent="center" mt={5}>
        <Typography>No saved teams found.</Typography>
      </Box>
    );
  }

  return (
    <Box display="flex" flexDirection="column" alignItems="center" mt={5}>
      <Typography variant="h4" mb={3}>
        {savedTeams.username}'s Saved Teams
      </Typography>
      <TeamCards teams={savedTeams.teams} />
    </Box>
  );
}
