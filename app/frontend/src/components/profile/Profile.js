import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';

class UserPage extends Component {
  state = {
    loading: false,
    loadingMinor: false,
    error: false,
    redirect: false,
    name: 'Jack'
  };

  render = () => {
    const name = this.state.name;
    return (
      <div className="Profile">
        <h1 className="h1-user">User page</h1>
        <h1 className="name">{name}</h1>
      </div>
    )
  }
}

export default withRouter(UserPage);