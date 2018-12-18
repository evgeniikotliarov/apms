import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './Signup.css';
import Application from "../../Application";


class SignUp extends Component {
  state = {
    email: '',
    fullname: '',
    password: '',
    errorMessage: null
  };

  render = () => {
    return (
      <div className="Signup">
        <h1 className="h1">Регистрация</h1>
        {this.renderErrorMessage()}
        <form>
          <label className="for-label">Email:</label>
          <input className="for-input" type="text" placeholder="Email"
                 onChange={this.onEmailFieldChange}
                 value={this.state.email}/>
          <label className="for-label">Имя:</label>
          <input className="for-input" type="text" placeholder="Name"
                 onChange={this.onFullnameFieldChange}
                 value={this.state.fullname}/>
          <label className="for-label">Пароль:</label>
          <input className="for-input" type="password" placeholder="Password"
                 onChange={this.onPasswordFieldChange}
                 value={this.state.password}/>
          <button className="btn-login"
                  onClick={this.onSignUpClick}
                  type="submit">Зарегистрироваться
          </button>
        </form>
        <span>Уже зарегистрированы?</span>
        <span onClick={this.onLoginClick} className="for-signup">Войти</span>
      </div>
    )
  };

  renderErrorMessage() {
    return this.state.errorMessage ?
      <div className="message">{this.state.errorMessage}</div> : null;
  }

  onEmailFieldChange = (event) => {
    this.setState({email: event.target.value});
  };

  onFullnameFieldChange = (event) => {
    this.setState({fullname: event.target.value});
  };

  onPasswordFieldChange = (event) => {
    this.setState({password: event.target.value});
  };

  onLoginClick = () => {
    this.props.history.push('/log-in')
  };

  onSignUpClick = (event) => {
    event.preventDefault();
    const data = {
      email: this.state.email,
      password: this.state.password,
      fullname: this.state.fullname
    };
    this.state.errorMessage = data.email && data.password ? null : data.email ? 'Введите пароль' :
      data.password ? 'Введите email' : 'Введите email и пароль';
    if (this.state.errorMessage) return;
    Application.userRepository.logIn(data.email, data.password);
    this.props.history.push('/profile')
  };
}

export default withRouter(SignUp);