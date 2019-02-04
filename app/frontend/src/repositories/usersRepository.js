const TOKEN = 'token';
const USERS = 'users';
const PROFILE = 'profile';
const TIME_SHEETS = 'timeSheets';

export default class UsersRepository {
  constructor(storage, api) {
    this.storage = storage;
    this.api = api;
  }

  logIn = (email, password) => {
    return this.api.logIn(email, password)
      .map(data => {
          this.storage.saveData(TOKEN, data[TOKEN]);
          return data;
        }
      );
  };

  signUp = (name, email, password) => {
    return this.api.signUp(name, email, password)
      .map(data => {
          this.storage.saveData(TOKEN, data[TOKEN]);
          return data;
        }
      )
  };

  logOut = () => {
    this.storage.removeData(TIME_SHEETS);
    this.storage.removeData(PROFILE);
    this.storage.removeData(TOKEN);
  };

  getProfileData = () => {
    const token = this.storage.loadData(TOKEN);
    return this.api.getProfile(token)
      .map(data => {
          this.storage.saveData(PROFILE, data);
          return data;
        }
      )
  };

  getUsers = () => {
    const token = this.storage.loadData(TOKEN);
    return this.api.getUsers(token)
      .map(data => {
          this.storage.saveData(USERS, data);
          return data;
        }
      )
  }
}