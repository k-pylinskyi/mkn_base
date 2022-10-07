import styled from "styled-components";
import { StyledContainer } from "../../styles/styledContainer";

export const HeaderWrapper = styled.div`
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    /* background: url('https://preview.redd.it/gkk5s1iw29oz.jpg?auto=webp&s=25d1287ec7e2c3c99364cba5ea8df82f42d72b30'); */
    /* background-position-y: 340px; */
    /* background-size: cover; */
    background-color: #2a2e2a;
    color: #ffffff;
`
export const StyledHeaderContainer = styled(StyledContainer)`
    display: flex;
    justify-content: space-between;
    .logo {
        color: #793f00;
        font-size: 32px;
        font-weight: 600;
        -webkit-text-stroke: 1px #37a61c;
        height: 100%;
        padding: 0 30px;
        img {
            max-height: 50px;
        }
    }
    .header {
        &__version {
            font-size: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0.5;
        }
    }
`