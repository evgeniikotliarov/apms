import React from 'react';

export default class UserEditingModalContent {
  constructor(user) {
    this.user = user;
  }

  renderHead() {
    return (
      <div>
        <p>HEAD</p>
      </div>
    )
  }

  renderContent(closeDialog) {
    return (
      <div>
        <p>{this.user.name}</p>
        <p>{this.user.email}</p>
        <p>{this.user.is_admin === true ? "Да" : "Нет"}</p>
        <p>{this.user.activated}</p>
        <button onClick={closeDialog}> close </button>
      </div>
    )
  }
}