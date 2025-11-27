import { LinearGradient } from "react-text-gradients";

interface Props {
  text: string;
}

export const LinearGradText = ({ text }: Props) => {
  return (
    <h3 style={{ padding: "10px 0px 10px 0px" }}>
      <LinearGradient
        gradient={["to left", "var(--secondary), var(--primary)"]}
        fallbackColor="var(--text)"
      >
        {text}
      </LinearGradient>
    </h3>
  );
};

export default LinearGradText;
