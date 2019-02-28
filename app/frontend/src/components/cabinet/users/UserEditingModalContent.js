import React from 'react';

export default class UserEditingModalContent {
  constructor(user) {
    this.user = user;
  }

  render() {
    return(
      <div>
        <p>{this.user.name}</p>
        <p>{this.user.email}</p>
        <p>{this.user.is_admin === true ? "Да" : "Нет"}</p>
        <p>{this.user.activated}</p>
      </div>
    )
  }
}