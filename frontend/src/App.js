import React from "react";
import HomePage from "./pages/home/HomePage";

import './App.css';
import {GlobalStyle} from "./components/styles/globalStyles";

function App() {
    return (
        <>
            <HomePage/>
            <GlobalStyle/>
        </>
    );
}

export default App;
