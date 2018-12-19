import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import Application from "../../Application";

class UserPage extends Component {
  constructor() {
    super();
    this.fetchProfile();
  }
  state = {
    name: null
  };

  render = () => {
    return (
      <div className="Profile">
        <h1 className="h1-user">User page</h1>
        <h1 className="name">{this.state.name}</h1>
      </div>
    )
  };

  fetchProfile = () => {
    Application.userRepository.getProfileData()
      .subscribe(profile => {
        this.setState({name: profile.name});
      })
  }
}

export default withRouter(UserPage);