import React from 'react';
import {withRouter} from 'react-router-dom';
import BaseCabinetPage from "../basePage";
import "./Users.css"
import Application from "../../../Application";

class UsersPage extends BaseCabinetPage {
  state = {
    users: [],
  };

  componentWillMount() {
    Application.userUseCase.getUsers()
      .subscribe(users => this.setState({users}))
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  renderContent = () => {
    const table = this.state.users.length ? (
      <table className="users-table">
        <thead>
        <tr>
          <th className="tdTh">Имя</th>
          <th className="tdTh">Активирован</th>
          <th className="tdTh">Тариф отпуска</th>
          <th className="tdTh">Всего отпускных дней</th>
          <th className="tdTh">Админ</th>
          <th className="tdTh">Норма рабочих дней</th>
          <th className="tdTh">Действия</th>
        </tr>
        </thead>
        <tbody>
        {this.state.users.map(user => (
          <tr key={user.user_id}>
            <td className="tdTd">{user.name}</td>
            <td className="tdTd">{user.activated === true ? 'Да' : 'Нет'}</td>
            <td className="tdTd">{user.rate === 0 ? "-" : user.rate}</td>
            <td className="tdTd">{user.vacation}</td>
            <td className="tdTd">{user.is_admin === true ? 'Да' : 'Нет'}</td>
            <td className="tdTd">Work_norm</td>
            <td className="tdTd">
              <button className="btn button-edit" onClick="">
                <i className="material-icons edit">edit</i>Редактировать
              </button>
              <button className="btn button-delete" onClick="">
                <i className="material-icons edit">delete</i>Удалить
              </button>
            </td>
          </tr>
        ))}
        </tbody>
      </table>
    ) : <div>Пользователей нет</div>;
    return (
      <div className="users">
        <h3>Таблица пользователей</h3>
        {table}
      </div>
    )
  };
}


export default withRouter(UsersPage);
