import Header from "./Header.tsx";
import Footer from "./Footer.tsx";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <Header />
      <Footer />
      <Outlet />
    </div>
  );
};

export default Layout;
