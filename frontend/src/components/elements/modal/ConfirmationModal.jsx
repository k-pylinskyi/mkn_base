import React from "react";
import Dialog from "rc-dialog";

import { StyledButton } from "../../styles/styledButton";

const ConfirmationModal = ({ message, handler, visible, setVisible, setLoading }) => {

  return (
    <Dialog
      visible={visible}
      wrapClassName="default-modal-wrapper default-modal-wrapper_confirm"
      animation="zoom"
      maskAnimation="fade"
      title="Confirm"
      closable={false}
      forceRender={false}
      className="default-modal confirm-modal"
    >
      <div className="default-modal__content confirm-modal__content">
        {message}
      </div>
      <div className="default-modal__footer">
        <StyledButton color="danger" onClick={() => {setVisible();setLoading(false)}}>
          No
        </StyledButton>
        <StyledButton
          color="success" onClick={() => {
          handler();
          setVisible(false);
        }}
        >
          Yes
        </StyledButton>
      </div>
    </Dialog>
  );

};

export default ConfirmationModal;
