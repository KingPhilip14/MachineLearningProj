// import { Navigate } from "react-router-dom";
// import { useContext } from "react";
// import AuthContext from "../../context/AuthContext.tsx";
import { Typography } from "@mui/material";

export default function SavedTeams() {
  // const { auth } = useContext(AuthContext);

  // if (!auth) {
  //   return <Navigate to="/login" />;
  // }

  return (
    <>
      <div className={"page-container"}>
        <Typography>This is the saved teams page</Typography>
      </div>
    </>
  );
}
