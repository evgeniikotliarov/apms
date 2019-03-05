import React, {Component} from 'react';
import Application from "../../../Application";
import './NavBar.css';

class NavBar extends Component {
  state = {
    login: ''
  };

  componentWillMount = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({login: profile.email});
      });
  };

  handleLogout = (event) => {
    event.preventDefault();
    Application.userUseCase.logOut();
    this.props.props.history.push("/log-in");
  };

  render = () => {
    return (
      <div className="Navbar">
        <ul className="navigation-bar">
          <li className="tab active-tab"><a href="/time-sheet">Time sheet</a></li>
          <li className="tab"><a href="/users">Users</a></li>
          <li className="tab"><a href="/statistics">Statistic</a></li>
          <li className="tab"><a href="/profile">Profile</a></li>
          <li className="log-box">
            <a className="login" href="#">{this.state.login}</a>
            <a className="log-out" href="/log-out" onClick={this.handleLogout}>Log out</a>
          </li>
        </ul>
      </div>
    )
  }
}

export default NavBar;