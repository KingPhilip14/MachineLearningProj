import "../../App.css";
import "./Layout.css";
import Header from "./Header.tsx";
import Footer from "./Footer.tsx";
import { Outlet } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import { createTheme, ThemeProvider } from "@mui/material";

const Layout = () => {
  const [isDark, setIsDark] = useState(false);

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: isDark ? "dark" : "light",
        },
      }),

    [isDark],
  );

  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      isDark ? "dark" : "light",
    );
  }, [isDark]);

  return (
    <>
      <div className={"app"}>
        <ThemeProvider theme={theme}>
          <Header isDark={isDark} setIsDark={setIsDark} />
          <Outlet />
          <Footer />
        </ThemeProvider>
      </div>
    </>
  );
};

export default Layout;
