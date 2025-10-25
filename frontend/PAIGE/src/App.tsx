import Header from "./components/layout/Header.tsx";
import Footer from "./components/layout/Footer.tsx";
import { ThemeProvider } from "styled-components";
import { GlobalStyles } from "./themes/GlobalStyles.tsx";
import { lightTheme, darkTheme } from "./themes/Themes.tsx";

function App() {
  // const [theme, setTheme] = useState("light");
  // const themeToggler = () => {
  //   theme === "light" ? setTheme("dark") : setTheme("light");
  // };

  return (
    // <ThemeProvider theme={theme === "light" ? lightTheme : darkTheme}>
    <>
      <Header />
      {/*<div className="alert alert-primary">*/}
      {/*  <Alert children={"Hello World"} />*/}
      {/*</div>*/}
      <Footer />
    </>
    // </ThemeProvider>
  );
}

export default App;
