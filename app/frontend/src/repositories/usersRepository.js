export default class UsersRepository {
  constructor(storage, api) {
    this.storage = storage;
    this.api = api;
  }

  logIn = (email, password) => {
    this.api.logIn(email, password)
      .subscribe((token) => {
        this.storage.saveData('token', token[token]);
        console.log(token);
      })
  };

  signUp = (name, email, password) => {
    this.api.signUp(name, email, password)
      .subscribe((token) => {
        this.storage.saveData('token', token[token])
      })
  };
}