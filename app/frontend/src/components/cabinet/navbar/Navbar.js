import React, {Component} from 'react';
import Application from "../../../Application";
import './Navbar.css';

class Navbar extends Component {
  state = {
    name: ''
  };

  componentWillMount = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({name: profile.name});
      });
  };
  render = () => {
    return (
      <div className="Navbar">
        <ul className="ul">
          <li className="li"><a href="#">My statistic</a></li>
          <li className="li"><a href="#">Other</a></li>
          <li className="li name"><a href="#">Logout</a>
            <span></span>
            <a href="#"> {this.state.name}</a></li>
        </ul>
      </div>
    )
  }
}

export default Navbar;