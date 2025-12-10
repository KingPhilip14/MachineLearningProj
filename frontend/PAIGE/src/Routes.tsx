import { createBrowserRouter } from "react-router-dom";
import Home from "./components/home/Home.tsx";
import About from "./components/about/About.tsx";
import PageNotFound from "./PageNotFound.tsx";
import Layout from "./components/layout/Layout.tsx";
import TeamConfig from "./components/team-config/TeamConfig.tsx";
import GeneratedTeam from "./components/generated-team/GeneratedTeam.tsx";
import Login from "./components/account-access/Login.tsx";
import Register from "./components/account-access/Register.tsx";
import SavedTeams from "./components/saved-teams/SavedTeams.tsx";

export const Routes = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/about",
        element: <About />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/register",
        element: <Register />,
      },
      {
        path: "/team-config",
        element: <TeamConfig />,
      },
      {
        path: "/generated-team",
        element: <GeneratedTeam />,
      },
      {
        path: "/saved-teams",
        element: <SavedTeams />,
      },
      {
        path: "*",
        element: <PageNotFound />,
      },
    ],
  },
]);
