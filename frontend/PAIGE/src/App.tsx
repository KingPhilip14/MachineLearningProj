import Header from "./components/layout/Header.tsx";
import Footer from "./components/layout/Footer.tsx";
import Home from "./components/Home.tsx";

function App() {
  // const [theme, setTheme] = useState("light");
  // const themeToggler = () => {
  //   theme === "light" ? setTheme("dark") : setTheme("light");
  // };

  return (
    <>
      <Header />
      <Home />
      <Footer />
    </>
  );
}

export default App;
