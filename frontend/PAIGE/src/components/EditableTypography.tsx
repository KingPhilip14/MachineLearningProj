import { useState, useRef } from "react";
import Typography, { type TypographyProps } from "@mui/material/Typography";

interface Props extends TypographyProps {
  givenText: string;
  maxLength?: number;
}

export default function EditableTypography({
  givenText,
  maxLength = 15,
  ...rest
}: Props) {
  const [text, setText] = useState(givenText);
  const ref = useRef<HTMLSpanElement>(null);

  // used to help with positoning the cursor when typing
  const getCaretOffset = () => {
    const selection = window.getSelection();

    if (!selection || selection.rangeCount === 0) return 0;

    const range = selection.getRangeAt(0);
    return range.startOffset;
  };

  // used to help with positoning the cursor when typing
  const setCaretOffset = (offset: number) => {
    const el = ref.current;

    if (!el) return;

    const selection = window.getSelection();
    const range = document.createRange();

    range.setStart(el.firstChild || el, offset);
    range.collapse(true);

    selection?.removeAllRanges();
    selection?.addRange(range);
  };

  const handleInput = (event: React.FormEvent<HTMLSpanElement>) => {
    const el = ref.current;

    if (!el) return;

    const caret = getCaretOffset();
    const newText = event.currentTarget.innerText;

    if (newText.length <= maxLength) {
      setText(event.currentTarget.innerText);
    } else {
      el.innerText = text;
    }

    requestAnimationFrame(() => {
      const safeOffset = Math.min(caret, el.innerText.length);
      setCaretOffset(safeOffset);
    });
  };

  return (
    <Typography
      {...rest}
      sx={{
        cursor: "text",
        ...(rest.sx || {}),
      }}
    >
      <span
        ref={ref}
        contentEditable
        suppressContentEditableWarning
        onInput={handleInput}
      >
        {text}
      </span>
    </Typography>
  );
}
