import React, {Component} from 'react';
import BaseModal from "../../common/BaseModal";

class ProfileInfo extends BaseModal {
  state = {
    showEditingUserModal: false
  };

  render = () => {
    return this.props.profile !== undefined ? (
      <div className="profile-info">
        <div className="user-data">
          <p>Имя пользователя:<span>{this.props.profile.name}</span></p>
        </div>
        <div className="user-data">
          <p>Email пользователя:<span>{this.props.profile.email}</span></p>
        </div>
        <div className="user-data">
          <p>Дата поступления:<span>{this.props.profile.employment_date}</span></p>
        </div>
        <div className="user-data">
          <p>Дата активации:<span>{this.props.profile.acceptance_date}</span></p>
        </div>
        <div className="user-data">
          <p>Активирован:<span>{this.props.profile.activated === true ? "Да" : "Нет"}</span></p>
        </div>
        <div className="user-data">
          <p>Админ:<span>{this.props.profile.is_admin === true ? "Да" : "Нет"}</span></p>
        </div>
        <div className="user-data">
          <p>Тариф отпуска:<span>{this.props.profile.rate}</span></p>
        </div>
        <div className="user-data">
          <p>Количество отпускных дней:<span>{this.props.profile.vacation}</span></p>
        </div>
        <div className="user-data">
          <button className="info-edit">Редактировать</button>
        </div>
      </div>
    ) : null
  }
}

export default ProfileInfo;
