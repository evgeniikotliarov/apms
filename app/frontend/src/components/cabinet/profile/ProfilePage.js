import React, {Component} from 'react';
import BaseCabinetPage from "../basePage";
import ProfileInfo from "./ProfileInfo";
import Application from "../../../Application";
import ProfileEditingModal from "./ProfileEditingModal";
import "./Profile.css";

class ProfilePage extends BaseCabinetPage {
  state = {
    showEditingUserModal: false,
    profile: undefined
  };

  componentWillMount() {
    this.fetchProfile();
  }

  fetchProfile() {
    this.setState({showEditingUserModal: false});
    Application.userUseCase.getProfile()
      .subscribe(profile => this.setState({profile}))
  }

  handleEdit(event) {
    event.preventDefault();
    this.setState({showEditingUserModal: true});
  }

  renderContent = () => {
    return (
      <div className="profile-page">
        <ProfileEditingModal
          updateMethod={() => this.fetchProfile()}
          showModal={this.state.showEditingUserModal}
          user={this.state.profile}/>
        <h1>Информация о пользователе</h1>
        <ProfileInfo profile={this.state.profile}/>

        <div className="user-data">
          <button className="info-edit" onClick={
            event => this.handleEdit(event)}>Редактировать</button>
        </div>
      </div>
    )
  }
}

export default ProfilePage;