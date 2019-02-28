import React from 'react';
import {withRouter} from 'react-router-dom';
import BaseCabinetPage from "../basePage";
import "./Users.css"
import Application from "../../../Application";
import UserEditingModalContent from "./UserEditingModalContent";

class UsersPage extends BaseCabinetPage {
  state = {
    users: [],
  };

  componentWillMount() {
    Application.userUseCase.getUsers()
      .subscribe(users => this.setState({users}))
  }

  handleEdit(event, user) {
    event.preventDefault();
    const content = new UserEditingModalContent(user);
    this.showModal(() => content.render());
  }

  renderContent = () => {
    const table = this.state.users.length ? (
      <table className="users-table">
        <thead>
        <tr>
          <th className="tdTh">Имя</th>
          <th className="tdTh">Ативирован</th>
          <th className="tdTh">Тариф отпуска</th>
          <th className="tdTh">Всего отпускных дней</th>
          <th className="tdTh">Амин</th>
          <th className="tdTh">Норма рабочих дней</th>
          <th className="tdTh">Действия</th>
        </tr>
        </thead>
        <tbody>
        {this.renderUsers()}
        </tbody>
      </table>
    ) : <div>Пользователей нет</div>;
    return (
      <div className="users">
        <h3>Список пользователей</h3>
        {table}
      </div>
    )
  };

  renderUsers() {
    return this.state.users.map(user => (
      <tr key={user.id}>
        <td className="tdTd">{user.name}</td>
        <td className="tdTd">{user.activated === true ? 'Да' : 'Нет'}</td>
        <td className="tdTd">{user.rate === 0 ? "-" : user.rate}</td>
        <td className="tdTd">{user.vacation === null ? '0' : user.vacation}</td>
        <td className="tdTd">{user.is_admin === true ? 'Да' : 'Нет'}</td>
        <td className="tdTd">Work_norm</td>
        <td className="tdTd">
          <button className="btn button-edit" onClick={event => this.handleEdit(event, user)}>
            <i className="material-icons edit">edit</i>Редактировать
          </button>
          <button className="btn button-more" onClick={event => {}}>
            <i className="material-icons edit">more_horiz</i>Подробнее
          </button>
        </td>
      </tr>
    ));
  }
}


export default withRouter(UsersPage);
