import "./Layout.css";
import Header from "./Header.tsx";
import Footer from "./Footer.tsx";
import { Outlet } from "react-router-dom";
// import { useColorScheme } from "@mui/material";
// import { Themes } from "../../themes/Themes.tsx";

const Layout = () => {
  // const colorScheme = useColorScheme();
  // const theme = Themes[colorScheme] ?? Themes.light;

  return (
    <div className={"page-container"}>
      <Header />
      <Outlet />
      <Footer />
    </div>
  );
};

export default Layout;
