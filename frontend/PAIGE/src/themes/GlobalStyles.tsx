import { createGlobalStyle } from "styled-components";

export const GlobalStyles = createGlobalStyle`
    body{
        background: ${({ theme }) => theme.background};
        color: ${({ theme }) => theme.text};
        font-family: Verdana, "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
        transition: all 0.5s linear;
    }
`;
