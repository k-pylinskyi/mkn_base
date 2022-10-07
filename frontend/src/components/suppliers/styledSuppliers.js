import styled from 'styled-components';
import { StyledContainer } from '../styles/styledContainer';
import {Table,TableHeader,TableBody,TableRow,TableCell} from "@fluentui/react-components/unstable"


export const StyledSuppliersContainer = styled(StyledContainer)`
`

export const SuppliersList = styled(Table)`
`

export const SuppliersListHead = styled(TableHeader)`
`

export const SuppliersListBody = styled(TableBody)`
    grid-template-columns: 1fr;
`

export const SupplersListRow = styled(TableRow)`
    display: grid;
    grid-template-columns: 100px 1fr 45px;
`

export const SuppliersListCol = styled(TableCell)`
    display: flex;
    justify-content: flex-start;
    align-items: center;
    .supplier_name {
        text-transform: capitalize;
    }
`