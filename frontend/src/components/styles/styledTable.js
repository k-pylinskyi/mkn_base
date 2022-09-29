import styled from "styled-components";

export const StyledTable = styled.div`
  width: calc(100% - 122px);
  margin: 30px 60px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 0, 0, 0.2);
`;

export const StyledTableHead = styled.div`
  width: 100%;
  color: #ffffff;
  display: grid;
  ${({ col }) => col && `grid-template-columns: repeat(${col}, 1fr)`};
  background: #3f3f3f;
`;

export const StyledTableHeadCol = styled.div`
  padding: 10px 15px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

export const StyledTableRow = styled.div`
  display: grid;
  ${({ col }) => col && `grid-template-rows: repeat(${col}, 1fr)`};
`;

export const StyledTableBody = styled.div`
  display: grid;
  ${({ col }) => col && `grid-template-columns: repeat(${col}, 1fr)`};
`

export const StyledTableCol = styled.div`
  padding: 10px 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  &:nth-child(2n) {
    background: rgba(0, 0, 0, 0.05);
  }
`;
