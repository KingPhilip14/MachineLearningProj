import { Link } from "react-router-dom";
import { Box, Container, Typography } from "@mui/material";
import "./Layout.css";

export default function Footer() {
  return (
    <Box component="footer" className={"footer"}>
      <Container maxWidth="lg">
        <Typography className={"footer-text"}>
          Report bugs or leave feedback by creating an issue on{" "}
          <Link
            className={"footer-link"}
            target={"_blank"}
            to={"https://github.com/KingPhilip14/MachineLearningProj/issues"}
          >
            GitHub
          </Link>
        </Typography>
        <Typography className={"footer-text"}>
          Pokémon is © of Nintendo, 1995-2025
        </Typography>
      </Container>
    </Box>
  );
}
