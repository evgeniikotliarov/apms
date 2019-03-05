import Rx from 'rxjs/Rx';
import axios from 'axios';

class UsersApi {
  constructor() {
    this.client = axios;
    this.client.defaults.withCredentials;
    this.client.defaults.headers.post['Content-Type'] = 'application/json';
    this.client.defaults.headers.post['Accept'] = 'application/json';
  }

  logIn(email, password) {
    const data = {email: email, password: password};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          'api/log-in',
          JSON.stringify(data)
        )
      )
      .map((response) => response.data)
  }

  signUp(name, email, password) {
    const data = {name: name, email: email, password:password};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          'api/sign-up',
          JSON.stringify(data)
        )
      )
      .map((response) => response.data)
  }

  getProfile(token) {
    return Rx.Observable
      .fromPromise(
        this.client.get(
          'api/profile', {
            headers: {Authorization: token}
          }
        )
      )
      .map((response) => response.data)
  }

  getUsers(token) {
    return Rx.Observable
      .fromPromise(
        this.client.get(
          'api/employees', {
            headers: {Authorization: token}
          }
        )
      )
      .map((response) => response.data);
  }

  getUser(token, userId) {
    return Rx.Observable
      .fromPromise(
        this.client.get(
          'api/employees/${userId}', {
            headers: {Authorization: token}
          }
        )
      )
      .map((response) => response.data);
  }

  updateProfile(token, name, email, oldPassword, newPassword) {
    const data = {name: name, email: email, oldPassword: oldPassword, newPassword: newPassword};
    return Rx.Observable
      .fromPromise(
        this.client.patch(
          'api/profile',
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.data);
  }
}

export default UsersApi;