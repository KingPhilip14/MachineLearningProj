import * as React from "react";
import { styled, alpha } from "@mui/material/styles";
import Button from "@mui/material/Button";
import Menu, { type MenuProps } from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import { useState } from "react";

interface Props {
  menuText: string;
  pkmnName: string;
  abilities: string[];
  onSelect: (ability: string) => void;
}

interface AbilityInfo {
  ability_name: string;
  is_hidden: boolean;
}

async function getAbilityData(pkmnName: string, ability: string) {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/pokemon-ability/by-name/${pkmnName}/${ability}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

    if (!response.ok) {
      throw new Error(
        `Unable to get ability data with Pokemon name ${pkmnName} and ability ${ability}`,
      );
    }

    return await response.json();
  } catch (error) {
    console.error(error);
  }
}

function normalizeAbilityName(ability: string): string {
  return ability.replace(" ", "-").toLowerCase();
}

function DisplayAbility(ability: string, info?: AbilityInfo) {
  if (!info) return ability;
  return info.is_hidden ? `${ability} (hidden ability)` : ability;
}

const StyledMenu = styled((props: MenuProps) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: "bottom",
      horizontal: "right",
    }}
    transformOrigin={{
      vertical: "top",
      horizontal: "right",
    }}
    {...props}
  />
))(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color: "rgb(55, 65, 81)",
    boxShadow:
      "rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px",
    "& .MuiMenu-list": {
      padding: "4px 0",
    },
    "& .MuiMenuItem-root": {
      "& .MuiSvgIcon-root": {
        fontSize: 18,
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
        ...theme.applyStyles("dark", {
          color: "inherit",
        }),
      },
      "&:active": {
        backgroundColor: alpha(
          theme.palette.primary.main,
          theme.palette.action.selectedOpacity,
        ),
      },
    },
    ...theme.applyStyles("dark", {
      color: theme.palette.grey[300],
    }),
  },
}));

export default function AbilityMenu({
  menuText,
  pkmnName,
  abilities,
  onSelect,
}: Props) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const [abilityInfo, setAbilityInfo] = useState<Record<string, AbilityInfo>>(
    {},
  );

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);

    // fetches the information of the ability the first time the menu opens
    if (Object.keys(abilityInfo).length === 0) {
      abilities.forEach(async (ability) => {
        const normalizedAbility = normalizeAbilityName(ability);
        const info = await getAbilityData(pkmnName, normalizedAbility);

        if (info) {
          setAbilityInfo((prev) => ({
            ...prev,
            [normalizedAbility]: info,
          }));
        }
      });
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <Button
        id="demo-customized-button"
        aria-controls={open ? "demo-customized-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        variant="contained"
        disableElevation
        onClick={handleClick}
        endIcon={<KeyboardArrowDownIcon />}
        sx={{ backgroundColor: "var(--secondary)", color: "var(--text)" }}
      >
        {menuText}
      </Button>
      <StyledMenu
        id="demo-customized-menu"
        slotProps={{
          list: {
            "aria-labelledby": "demo-customized-button",
          },
        }}
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
      >
        {abilities.map((ability) => {
          const normalized = normalizeAbilityName(ability);
          const info = abilityInfo[normalized];

          return (
            <MenuItem
              key={ability}
              onClick={() => {
                onSelect(ability);
                handleClose();
              }}
              disableRipple
            >
              {DisplayAbility(ability, info)}
            </MenuItem>
          );
        })}
      </StyledMenu>
    </div>
  );
}
