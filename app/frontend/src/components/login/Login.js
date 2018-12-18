import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './Login.css'
import Application from "../../Application";

class Login extends Component {
  state = {
    email: '',
    password: '',
    errorMessage: null
  };

  render = () => {
    return (
      <div className="Login">
        {this.renderErrorMessage()}
        <h1 className="h1-login">Войти</h1>
        <form>
          <label className="for-label">Email</label>
          <input className="for-input" type="text" placeholder="Email"
                 onChange={this.onEmailFieldChange}
                 value={this.state.email}/>
          <label className="for-label">Password</label>
          <input className="for-input"
                 type="password" placeholder="Password"
                 onChange={this.onPasswordFieldChange}
                 value={this.state.password}/>
          <button className="btn-login" onClick={this.onLoginClick} type="submit">Войти</button>
        </form>
        <span onClick={this.onSignupClick} className="for-signup">Регистрация</span>
      </div>
    )
  };

  renderErrorMessage() {
    return this.state.errorMessage ?
      <div className="message">{this.state.errorMessage}</div> : null;
  }

  onEmailFieldChange = (event) => {
    const email = event.target.value;
    this.setState({email});
  };

  onPasswordFieldChange = (event) => {
    const password = event.target.value;
    this.setState({password});
  };

  onLoginClick = (event) => {
    event.preventDefault();
    const data = {email: this.state.email, password: this.state.password};
    this.state.errorMessage = data.email && data.password ? null : data.email ? 'Введите пароль' :
      data.password ? 'Введите email' : 'Введите email и пароль';
    if (this.state.errorMessage) return;
    Application.userRepository.logIn(data.email, data.password);
    this.props.history.push('/profile');
  };

  onSignupClick = () => {
    this.props.history.push('/sign-up');
  };
}

export default withRouter(Login);