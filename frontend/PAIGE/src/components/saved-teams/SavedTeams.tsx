import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.tsx";
import { Typography } from "@mui/material";

interface TeamProps {
  account_id: number;
  team_name: string;
  generation: string;
}

export default function SavedTeams() {
  const { auth } = useAuth();

  if (!auth) {
    return <Navigate to="/login" />;
  }

  return (
    <>
      <div className={"page-container"}>
        <Typography>This is the saved teams page</Typography>
      </div>
    </>
  );
}
