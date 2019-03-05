import React from 'react';
import Application from "../../../Application";
import BaseModal from "../../common/BaseModal";

export default class ProfileEditingModal extends BaseModal {
  needToShowPasswordBlock = true;

  state = {
    name: undefined,
    email: undefined,
    oldPassword: undefined,
    newPassword: undefined,
    acceptPassword: undefined,
  };

  head() {
    return (
      <div>
        <h4>Редактирование пользователя</h4>
      </div>
    );
  }

  content() {
    this.initStates();
    return (
      <div>
        <form className="form">
          <label>Имя</label>
          <input
            id="user-name"
            type="text"
            value={this.state.name}
            ref="name"
            onChange={event => this.setState({name: event.target.value})}
          />
          <label>Email</label>
          <input
            id="user-email"
            type="text"
            value={this.state.email}
            ref="email"
            onChange={event => this.setState({email: event.target.value})}
          />
        </form>
        <div className="change-password">
          <button onClick={() => {
            document.getElementById('passwords').style.display = this.needToShowPasswordBlock ?
              "block" : "none";
            this.needToShowPasswordBlock = !this.needToShowPasswordBlock;
          }
          }>Сменить пароль
          </button>

          <div id="passwords">
            <form className="form">
              <input
                id="user-old-password"
                type="password"
                value={this.state.oldPassword}
                placeholder="Введите старый пароль:"
                onChange={event => this.setState({oldPassword: event.target.value})}
              />
              <input
                id="user-new-password"
                type="password"
                value={this.state.newPassword}
                placeholder="Введите новый пароль:"
                onChange={event => this.setState({newPassword: event.target.value})}
              />
              <input
                type="password"
                id="user-accept-password"
                value={this.state.acceptPassword}
                placeholder="Подтвердите новый пароль:"
                onChange={event => this.setState({acceptPassword: event.target.value})}
              />
            </form>
          </div>
        </div>
      </div>
    );
  }

  foot() {
    return (
      <div className="control">
        <button onClick={event => this.onSubmit()} type="submit">Сохранить</button>
        <button onClick={() => this.close()}>Отмена
        </button>
      </div>
    );
  }

  onSubmit() {
    if (this.state.newPassword !== this.state.acceptPassword) {
      alert('encorrect');
    }
    const correctFillPassword = this.state.newPassword === this.state.acceptPassword;
    if (this.needToShowPasswordBlock && !correctFillPassword) {
      //TODO notify about error
    } else {
      Application.userUseCase.updateProfile(
        this.state.name,
        this.state.email,
        this.state.oldPassword,
        this.state.newPassword)
        .subscribe(() => {
          this.props.updateMethod();
          this.close();
        });
    }
  }

  initStates() {
    if (!this.props.user) return;
    this.state.name = this.state.name !== undefined ? this.state.name : this.props.user.name;
    this.state.email = this.state.email !== undefined ? this.state.email : this.props.user.email;
  }

  close() {
    super.close();
    this.resetStates();
  }

  resetStates() {
    if (!this.props.user) return;
    this.state.name = undefined;
    this.state.email = undefined;
  }
}
