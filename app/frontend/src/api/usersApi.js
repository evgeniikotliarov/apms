import Rx from 'rxjs/Rx';
import axios from 'axios';



class UsersApi {
  constructor() {
    this.client = axios;
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

  getUsers(userId) {
    return Rx.Observable
      .fromPromise(
        this.client.get('api/employees'))
      .map((response) => response.data);
  }

  getUser(userId) {
    return Rx.Observable
      .fromPromise(
        this.client.get(`api/employees/${userId}`))
      .map((response) => response.data)
  }
}

export default UsersApi;