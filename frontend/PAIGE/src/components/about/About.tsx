import "./About.css";
import "../../App.css";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import { createTheme, ThemeProvider } from "@mui/material";

export default function About() {
  const theme = createTheme({
    typography: {
      body1: {
        fontWeight: "bold",
        fontSize: "20px",
        padding: "10px 10px 10px 25px",
      },
      body2: {
        fontWeight: "inherit",
        fontSize: "16px",
        padding: "10px 10px 10px 25px",
      },
    },
  });

  return (
    <>
      <ThemeProvider theme={theme}>
        <Card style={{ width: "80%", margin: "50px" }}>
          <CardContent>
            <Typography variant="body1">What is PAIGE?</Typography>
            <Typography variant="body2" display={"block"}>
              PAIGE is the "<b>P</b>okémon <b>AI</b> <b>G</b>eneration <b>E</b>
              ngine",
            </Typography>
          </CardContent>
        </Card>
        {/*<div className={"about-page-container"}>*/}
        {/*  <div className="rounded-rectangle" style={{ width: "80%" }}>*/}
        {/*    <Typography variant="body1">What is PAIGE?</Typography>*/}

        {/*    <Typography variant="body2" display={"block"}>*/}
        {/*      PAIGE is the "<b>P</b>okémon <b>AI</b> <b>G</b>eneration <b>E</b>*/}
        {/*      ngine",*/}
        {/*    </Typography>*/}
        {/*  </div>*/}
        {/*</div>*/}
      </ThemeProvider>
    </>
  );
}
