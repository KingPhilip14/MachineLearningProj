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
      <ThemeProvider theme={theme}>
        <div className="min-h-[100dvh] grid grid-rows-[auto_1fr_auto] app">
          <Header isDark={isDark} setIsDark={setIsDark} />

          <main className="body">
            <Outlet />
          </main>

          <Footer />
        </div>
      </ThemeProvider>
    </>
  );
};

export default Layout;
