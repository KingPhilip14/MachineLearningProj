import "./Layout.css";
import Header from "./Header.tsx";
import Footer from "./Footer.tsx";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className={"page-container"}>
      <Header />
      <Outlet />
      <Footer />
    </div>
  );
};

export default Layout;
