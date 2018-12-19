export default class UsersRepository {
  constructor(storage, api) {
    this.storage = storage;
    this.api = api;
  }

  logIn = (email, password) => {
    return this.api.logIn(email, password)
      .map(token => this.storage.saveData('token', token[token])
      );
  };

  signUp = (name, email, password) => {
    return this.api.signUp(name, email, password)
      .map(token => this.storage.saveData('token', token[token]))
  };
}