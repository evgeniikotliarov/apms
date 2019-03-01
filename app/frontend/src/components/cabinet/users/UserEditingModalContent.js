import React from 'react';
import BaseModalContentRender from "../../common/ModalContentRender";

export default class UserEditingModal extends BaseModalContentRender{
  constructor(user) {
    super();
    this.user = user;
  }

  head() {
    return (
      <div>
        <h4>Редактирование пользователя</h4>
      </div>
    );
  }

  content() {
    return (
      <div>
        <p>{this.user.name}</p>
        <p>{this.user.email}</p>
        <p>{this.user.is_admin === true ? "Да" : "Нет"}</p>
        <p>{this.user.activated}</p>
      </div>
    );
  }

  foot() {
    return (
      <div className="control">
        <button onClick={event => this.onSubmit()} type="submit">Сохранить</button>
        <button onClick={event => this.dialog.close()}>Отмена</button>
      </div>
    )
  }

  onSubmit() {
    this.dialog.close();
  }
}
