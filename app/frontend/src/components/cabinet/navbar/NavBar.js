import React, {Component} from 'react';
import Application from "../../../Application";
import './NavBar.css';
import Logout from "./Logout";

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
          <li className="tab active-tab"><a href="/profile">Time sheet</a></li>
          <li className="tab"><a href="/users">Users</a></li>
          <li className="tab"><a href="#">Statistic</a></li>
          <li className="log-box">
            <a className="login" href="#">{this.state.login}</a>
            <span/>
            <a className="log-out" href="/">
              <Logout handleLogout={this.handleLogout}/>
            </a>
          </li>
        </ul>
      </div>
    )
  }
}

export default NavBar;