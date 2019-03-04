import React, {Component} from 'react';
import BaseModal from "../../common/BaseModal";

class ProfileInfo extends BaseModal {
  state = {
    showEditingUserModal: false
  };

  render = () => {
    return this.props.profile !== undefined ? (
      <div className="profile-info">
        <h2>Hello</h2>
        <div>
          <p>Имя пользователя:</p>
          <p>{this.props.profile.name}</p>
        </div>
      </div>
    ) : null
  }
}

export default ProfileInfo;