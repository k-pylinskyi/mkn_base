import React from "react";

import { StyledFilterWrapper } from "./styledFilter";
import { StyledButton } from "../../styles/styledButton";

const Filter = ({ createItem }) => {
  return (
    <StyledFilterWrapper>
        <StyledButton 
            color="main"
        >
            Filter
        </StyledButton>
      {createItem && <StyledButton color="main">Create item</StyledButton>}
    </StyledFilterWrapper>
  );
};

export default Filter;
