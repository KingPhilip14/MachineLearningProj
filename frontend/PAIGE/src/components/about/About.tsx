import "./About.css";
import "../../App.css";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import { createTheme, ThemeProvider } from "@mui/material";
import LinearGradText from "../LinearGradText.tsx";

export default function About() {
  // custom theming for this page (follows Q&A format)
  const theme = createTheme({
    typography: {
      body1: {
        fontWeight: "bold",
        fontSize: "20px",
        padding: "10px 0px 5px 25px",
        margin: "10px 10px 0px 0px",
        color: "var(--text)",
      },
      body2: {
        fontWeight: "inherit",
        fontSize: "16px",
        padding: "10px 10px 10px 25px",
        margin: "0px 10px 30px 0px",
        color: "var(--text)",
      },
    },
  });

  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="page-container">
          <LinearGradText text={"About"} />

          <Card
            className={"text-card about"}
            style={{ width: "80%", margin: "50px", borderRadius: "30px" }}
            sx={{ background: "var(--tertiary)" }}
          >
            <CardContent>
              <Typography variant="body1">What is PAIGE?</Typography>
              <Typography variant="body2" display={"block"}>
                PAIGE is the "<b>P</b>okémon <b>AI</b> <b>G</b>eneration{" "}
                <b>E</b>
                ngine." Simply put, it's a passion project that is a Pokémon
                team generator.
              </Typography>

              <Typography variant="body1">What is it used for?</Typography>
              <Typography variant="body2">
                This is used to generate a team of Pokémon using AI techniques.
                Will the teams be good? Not always, but that's the fun part.
                This was designed in a way for you to generate a fairly balanced
                team with some Pokémon you normally wouldn't use or think of
                using (like Wigglytuff).
              </Typography>

              <Typography variant="body1">
                So.. why am I using this instead of other team generators?
              </Typography>
              <Typography variant="body2">
                The algorithms used go beyond complete random team generation.
                Pokémon types, the role they could play in battle, and overall
                team composition are analyzed as teams are generated. The
                generator won't care for what is currently meta or what is
                "top-tier." Once it picks its first Pokémon for the team, it
                will pick others that will complement it and its weaknesses to
                created a balanced team.
                <br />
                <br />
                Furthermore, since this is a passion project, more features may
                be added to improve the team generation. This will create a
                dynamic experience to have fun with the pocket creatures we've
                come to love.
              </Typography>

              <Typography variant="body1">
                How can I use generated teams?
              </Typography>
              <Typography variant="body2">
                You have the option to export a generated team in a text format
                that can be imported to Pokémon Showdown. The battle format to
                use is "<em>gen9nationaldexag</em>" to ensure all Pokémon in
                your team can be used.
                <br />
                <br />
                *Please note that EVs, IVs, and items are not currently
                generated, but this may become a included in a future update.
              </Typography>

              <Typography variant="body1">
                Can I store generated teams?
              </Typography>
              <Typography variant="body2">
                Yes! All you need to do is create an account if you haven't
                already. No email is required for this -- simply a username and
                password. When logged in to an account and a team is generated,
                you can click "Save Team". That team will then be stored under
                that account to reference later in the Saved Teams page. If you
                don't save the team that is generated, it will be lost forever,
                so make sure you evaluate the team carefully!
              </Typography>
            </CardContent>
          </Card>
        </div>
      </ThemeProvider>
    </>
  );
}
