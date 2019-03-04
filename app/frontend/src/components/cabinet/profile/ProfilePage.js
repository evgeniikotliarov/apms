import React, {Component} from 'react';
import BaseCabinetPage from "../basePage";
import ProfileInfo from "./ProfileInfo";
import "./Profile.css";
import Application from "../../../Application";

class ProfilePage extends BaseCabinetPage {
  state = {
    profile: undefined
  };

  componentWillMount() {
    Application.userUseCase.getProfile()
      .subscribe(profile => this.setState({profile}))
  }

  renderContent = () => {
    return (
      <div className="profile-page">
        <h1>Информация о пользователе</h1>
        <ProfileInfo profile={this.state.profile}/>
      </div>
    )
  }
}

export default ProfilePage