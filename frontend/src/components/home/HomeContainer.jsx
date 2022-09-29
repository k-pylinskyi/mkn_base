<<<<<<< HEAD
import {StyledHomeContainer} from "./styledHome";

const HomeContainer = () => {
    return(
        <StyledHomeContainer>
            <h1>
                Home
            </h1>
        </StyledHomeContainer>
    )
}

export default HomeContainer;
=======
import {
  StyledTable,
  StyledTableBody,
  StyledTableCol,
  StyledTableHead,
  StyledTableRow,
  StyledTableHeadCol,
} from "../styles/styledTable";

const HomeContainer = ({ paketo }) => {
  return (
    <>
      {paketo && (
        <StyledTable>
          <StyledTableHead col={Object.keys(paketo).length}>
            {paketo &&
              Object.keys(paketo).map((value, key) => (
                <StyledTableHeadCol key={key}>
                  {value[0].toUpperCase() +
                    value.replace("_", " ").substring(1)}
                </StyledTableHeadCol>
              ))}
          </StyledTableHead>
          <StyledTableBody col={Object.keys(paketo).length}>
            {paketo &&
              Object.values(paketo).map((value) => (
                <StyledTableRow>
                  {Object.values(value).map((value, key) => (
                    <StyledTableCol key={key}>{value}</StyledTableCol>
                  ))}
                </StyledTableRow>
              ))}
          </StyledTableBody>
        </StyledTable>
      )}
    </>
  );
};

export default HomeContainer;
>>>>>>> b1ea73f (added frontend and app; changed Extractor.py)
