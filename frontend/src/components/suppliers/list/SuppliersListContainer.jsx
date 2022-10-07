import React, { useState, useEffect } from "react";
import axios from "axios";
import Filter from "../../elements/filter/FilterContianer";
import ConfirmationModal from "../../elements/modal/ConfirmationModal";

import {
  SuppliersListHead,
  StyledSuppliersContainer,
  SuppliersList,
  SuppliersListBody,
  SupplersListRow,
  SuppliersListCol,
} from "../styledSuppliers";
import { Button, Checkbox, Tooltip } from "@fluentui/react-components";
import { TableHeaderCell } from "@fluentui/react-components/unstable";
import { EditFilled } from "@fluentui/react-icons";

const SuppliersListContainer = () => {
  const [suppliers, setSuppliers] = useState({});
  const [loading, setLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const [status, setStatus] = useState();
  const [editSupplier, setEditSupplier] = useState();

  const handleChange = (value) => {
    setLoading(true);
    setVisible(true);
    setStatus(value.target.checked);
    setEditSupplier(value.target.supplier);
  };

  const fetchSuppliers = () => {
    axios
      .get("/suppliers")
      .then((response) => {
        response.data.map((supplier) =>
          setSuppliers((prevState) => ({
            ...prevState,
            [supplier.name]: supplier.status,
          }))
        );
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const modalVisible = () => {
    setVisible(false);
  };

  const updateStatus = () => {
    setLoading(true);
    axios
      .post("/suppliers", {
        status: status,
        supplier: editSupplier,
      })
      .then((response) => {
        setLoading(false);
        setSuppliers((prevState) => ({
          ...prevState,
          [response.data.supplier]: response.data.status,
        }));
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSuppliers();
  }, []);
  return (
    <>
      <ConfirmationModal
        setLoading={setLoading}
        visible={visible}
        setVisible={() => modalVisible()}
        message={
          "Do you want to change activity status of " + editSupplier + "?"
        }
        handler={() => updateStatus()}
      />
      <StyledSuppliersContainer>
        <h1>Suppliers list</h1>
        <Filter createItem />
        <SuppliersList>
          <SuppliersListHead>
            <SupplersListRow>
              <TableHeaderCell>Active</TableHeaderCell>
              <TableHeaderCell>Supplier name</TableHeaderCell>
              <TableHeaderCell />
            </SupplersListRow>
          </SuppliersListHead>
          <SuppliersListBody>
            {suppliers &&
              Object.keys(suppliers).map((supplier, key) => (
                <SupplersListRow key={key}>
                  <SuppliersListCol>
                    <Checkbox
                      disabled={loading}
                      supplier={supplier}
                      checked={suppliers[supplier]}
                      onChange={(value) => handleChange(value)}
                    />
                  </SuppliersListCol>
                  <SuppliersListCol className="supplier_name">
                    <div className="supplier_name">
                      {supplier.replace("_", " ")}
                    </div>
                  </SuppliersListCol>
                  <SuppliersListCol>
                    <Tooltip content="Edit supplier" relationship="label">
                      <Button
                        appearance="subtle"
                        shape="circular"
                        icon={<EditFilled />}
                        size="small"
                      />
                    </Tooltip>
                  </SuppliersListCol>
                </SupplersListRow>
              ))}
          </SuppliersListBody>
        </SuppliersList>
      </StyledSuppliersContainer>
    </>
  );
};

export default SuppliersListContainer;
