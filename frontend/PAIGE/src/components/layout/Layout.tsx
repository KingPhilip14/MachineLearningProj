import "../../App.css";
import "./Layout.css";
import Header from "./Header.tsx";
import Footer from "./Footer.tsx";
import { Outlet } from "react-router-dom";
import { Toggle } from "../toggle/Toggle.tsx";
import { useState } from "react";

const Layout = () => {
  const [isDark, setIsDark] = useState(false);

  return (
    <>
      <div className={"app"} data-theme={isDark ? "dark" : "light"}>
        <Header />
        <Toggle isChecked={isDark} handleChange={() => setIsDark(!isDark)} />
        <Outlet />
        <Footer />
      </div>
    </>
  );
};

export default Layout;
