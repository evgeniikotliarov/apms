import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import UsersApi from '../../api/usersApi';
import './Login.css'

class Login extends Component {
  state = {
    email: '',
    password: '',
    errorMessage: null
  };

  onEmailFieldChange = (event) => {
    const email = event.target.value;
    this.setState({email});
  };

  onPasswordFieldChange = (event) => {
    const password = event.target.value;
    this.setState({password});
  };

  onLoginClick = (e) => {
    e.preventDefault();
    const data = {email: this.state.email, password: this.state.password};
    this.state.errorMessage = data.email && data.password ? null : data.email ? 'Введите пароль' :
      data.password ? 'Введите email' : 'Введите email и пароль';
    if (this.state.errorMessage) return;
    const api = new UsersApi();
    api.logIn(data.email, data.password)
      .subscribe((x) => {
          // TODO save to tokenStorage
          console.log(x);
          this.props.history.push('/profile')
        }
      );
  };

  onSignupClick = () => {
    this.props.history.push('/sign-up');
  };

  render = () => {
    const message = this.state.errorMessage ?
      <div className="message">{this.state.errorMessage}</div> : null;
    return (
      <div className="Login">
        {message}
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
  }
}

export default withRouter(Login);