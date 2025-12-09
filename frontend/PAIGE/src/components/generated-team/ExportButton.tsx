import Button from "@mui/material/Button";

interface Props {
  content: string;
}

const ExportButton = ({ content }: Props) => {
  const handleDownload = () => {
    const fileName = "my-file.txt";
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);

    link.click();

    URL.revokeObjectURL(url);
    document.body.removeChild(link);
  };

  return <Button onClick={handleDownload}>Export Team</Button>;
};

export default ExportButton;
