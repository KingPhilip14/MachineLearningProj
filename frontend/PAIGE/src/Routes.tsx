import { createBrowserRouter } from "react-router-dom";
import Home from "./components/home/Home.tsx";
import About from "./components/about/About.tsx";
import PageNotFound from "./PageNotFound.tsx";
import Layout from "./components/layout/Layout.tsx";
import TeamConfig from "./components/team-config/TeamConfig.tsx";
import GeneratedTeam from "./components/generated-team/GeneratedTeam.tsx";

export const Routes = createBrowserRouter([
  {
    // path: "/",
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
        path: "/team-config",
        element: <TeamConfig />,
      },
      {
        path: "/generated-team",
        element: <GeneratedTeam />,
      },
      {
        path: "*",
        element: <PageNotFound />,
      },
    ],
  },
]);
