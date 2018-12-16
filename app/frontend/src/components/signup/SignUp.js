import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import './SignUp.css';


class Signup extends Component {

  state = {
    email: '',
    fullname: '',
    password: '',
    errorMessage: null,
    loading: true
  };

  emailChange = (e) => {
    this.setState({email: e.target.value});
  };

  fullnameChange = (e) => {
    this.setState({fullname: e.target.value});
  };

  passwordChange = (e) => {
    this.setState({password: e.target.value});
  };

  onLoginClick = () => {
    this.props.history.push('/')
  };

  render = () => {
    const message = this.state.errorMessage ? <div className="message">{ this.state.errorMessage }</div> : null;
    return (
      <div className="Signup">
        <h1 className="h1">Регистрация</h1>
        { message }
        <form>
          <label className="for-label">Email:</label>
          <input className="for-input" type="text" placeholder="Email"
                 onChange={this.emailChange}
                 value={this.state.email}/>
          <label className="for-label">Имя:</label>
          <input className="for-input" type="text" placeholder="Name"
                 onChange={this.fullnameChange}
                 value={this.state.fullname}/>
          <label className="for-label">Пароль:</label>
          <input className="for-input" type="password" placeholder="Password"
                 onChange={this.passwordChange}
                 value={this.state.password}/>
          <button className="btn-login"
                  onClick={this.onSignupClick}
                  type="submit">Зарегистрироваться</button>
        </form>
        <span>Уже зарегистрированы?</span>
        <span onClick={this.onLoginClick} className="for-signup">Войти</span>
      </div>
    )
  }
}

export default withRouter(Signup);