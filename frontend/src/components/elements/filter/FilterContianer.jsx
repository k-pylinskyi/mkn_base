import React from "react";

import { StyledFilterWrapper } from "./styledFilter";
import { Button } from "@fluentui/react-components";

const Filter = ({ createItem }) => {
  return (
    <StyledFilterWrapper>
        <Button 
            appearance="primary"
        >
            Filter
        </Button>
      {createItem && <Button appearance="primary">Create item</Button>}
    </StyledFilterWrapper>
  );
};

export default Filter;
