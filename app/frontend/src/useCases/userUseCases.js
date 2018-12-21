export default class UsersUseCase {
  constructor(repository) {
    this.repository = repository;
  }

  logIn(email, password) {
    return this.repository.logIn(email, password);
  }

  signUp(name, email, password) {
    return this.repository.signUp(name, email, password);
  }

  getProfile() {
    return this.repository.getProfileData();
  }
}