import { Box, Container, Typography } from "@mui/material";

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        background: "linear-gradient(45deg, #1f271b, #0b4f6c)",
        py: 1,
        mt: "auto",
        position: "fixed",
        bottom: 0,
        width: "100%",
      }}
    >
      <Container maxWidth="lg">
        <Typography align="center" style={{ color: "white" }}>
          Report bugs or leave feedback by creating an issue on <a />
          <a
            href={"https://github.com/KingPhilip14/MachineLearningProj/issues"}
          >
            GitHub
          </a>
        </Typography>
        <Typography align="center" style={{ color: "white" }}>
          Pokémon is © of Nintendo, 1995-2025
        </Typography>
      </Container>
    </Box>
  );
}
