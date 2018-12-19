const TOKEN = 'token';
const PROFILE = 'profile';

export default class UsersRepository {
  constructor(storage, api) {
    this.storage = storage;
    this.api = api;
  }

  logIn = (email, password) => {
    return this.api.logIn(email, password)
      .map(data =>
        this.storage.saveData(TOKEN, data[TOKEN])
      );
  };

  signUp = (name, email, password) => {
    return this.api.signUp(name, email, password)
      .map(data =>
        this.storage.saveData(TOKEN, data[TOKEN]))
  };

  getProfileData = () => {
    const token = this.storage.loadData(TOKEN);
    return this.api.getProfile(token)
      .map(data => {
        this.storage.saveData(PROFILE, data);
        return data
      }
    )
  };
}