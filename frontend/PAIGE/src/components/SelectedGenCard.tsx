import { CardActions, Typography } from "@mui/material";
import CardContent from "@mui/material/CardContent";
import { Link } from "react-router-dom";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";

interface Props {
  selectedGen: string;
  backPage: string;
}

export const SelectedGenCard = ({ selectedGen, backPage }: Props) => {
  return (
    <Card
      className={"text-card"}
      style={{ flexDirection: "column" }}
      sx={{
        height: "160px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        borderRadius: "30px",
        background: "var(--tertiary)",
        marginBottom: "50px",
      }}
    >
      <CardContent>
        <Typography
          variant="h5"
          style={{ textAlign: "center", margin: 0, lineHeight: 1.4 }}
        >
          Selected generation: {selectedGen}
        </Typography>
      </CardContent>
      <CardActions>
        <Link to={backPage} state={{ selectedGen: selectedGen }}>
          <Button
            variant={"outlined"}
            size={"large"}
            sx={{ borderColor: "var(--text)", color: "var(--text)" }}
          >
            Back
          </Button>
        </Link>
      </CardActions>
    </Card>
  );
};
