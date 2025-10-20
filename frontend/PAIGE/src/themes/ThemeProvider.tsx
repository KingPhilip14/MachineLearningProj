// import { createContext, useState } from "react";
// import { LightTheme } from "./LightTheme.js";
// import { DarkTheme } from "./DarkTheme.js";
//
// const ThemeContext = createContext("light");
//
// export const ThemeProvider = ({ children }) => {
//   const [theme, setTheme] = useState(LightTheme);
//
//   const toggleTheme = () => {
//     setTheme((previousTheme) =>
//       previousTheme === LightTheme ? DarkTheme : LightTheme,
//     );
//   };
//
//   return (
//     <ThemeContext.Provider value={{ theme, toggleTheme }}>
//       {children}
//     </ThemeContext.Provider>
//   );
// };
