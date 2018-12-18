import usersApi from "./api/usersApi";
import StorageAdapter from "./storage/StorageAdapter";
import Application from "./Application";
import UsersRepository from "./repositories/usersRepository";

export default class ApplicationFabric {
  createApplication() {
    this.usersApi = new usersApi();
    this.storage = new StorageAdapter();

    const usersRepository = new UsersRepository(this.storage, this.usersApi);
    return new Application(usersRepository);
  }
}