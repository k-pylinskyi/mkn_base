import React from "react";
import HomePage from "../pages/home/HomePage";
import SuppliersPage from "../pages/suppliers/SuppliersPage";
import CreateSupplierPage from "../pages/suppliers/CreateSupplierPage"

const routes = [
    {
        title: "Home page",
        path: "/",
        exact: true,
        component: HomePage
    },
    {
        title: "Suppliers list",
        path: "/suppliers",
        exact: true,
        component: SuppliersPage
    },
    {
        title: "Create supplier",
        path: "/suppliers/create",
        exact: false,
        component: CreateSupplierPage
    }
]

export default routes