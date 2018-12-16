import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import './Login.css'

class Login extends Component {

  state = {
    email: '',
    password: '',
    errorMessage: null
  };

  emailChange = (event) => {
    const email = event.target.value;
    this.setState({email});
  };

  passwordChange = (event) => {
    const password = event.target.value;
    this.setState({password});
  };

  onLoginClick = (e) => {
    e.preventDefault();
    const credentials = {"email": this.state.email, "password": this.state.password};
    if (!credentials.email && !credentials.password) {
      this.setState({errorMessage: 'Введите email и пароль'})
    } else if (!credentials.email) {
      this.setState({errorMessage: 'Введите email'})
    } else if (!credentials.password) {
      this.setState({errorMessage: 'Введите пароль'})
    }
  };

  onSignupClick = () => {
    this.props.history.push('/sign-up');
  };

  render = () => {
    const message = this.state.errorMessage ? <div className="message">{this.state.errorMessage}</div> : null;
    return (
      <div className="Login">
        { message }
        <h1 className="h1-login">Войти</h1>
        <form>
          <label className="for-label">Email</label>
          <input className="for-input" type="text" placeholder="Email"
                 onChange={this.emailChange}
                 value={this.state.email}/>
          <label className="for-label">Password</label>
          <input className="for-input"
                 type="password" placeholder="Password"
                 onChange={this.passwordChange}
                 value={this.state.password}/>
          <button className="btn-login" onClick={this.onLoginClick} type="submit">Войти</button>
        </form>
        <span onClick={this.onSignupClick} className="for-signup">Регистрация</span>
      </div>
    )
  }
}

export default withRouter(Login);