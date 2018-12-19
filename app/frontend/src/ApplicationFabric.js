import UsersApi from "./api/usersApi";
import StorageAdapter from "./storage/StorageAdapter";
import UsersRepository from "./repositories/usersRepository";
import Application from "./Application";

export default class ApplicationFabric {
  createApplication() {
    this.usersApi = new UsersApi();
    this.storage = new StorageAdapter();

    const usersRepository = new UsersRepository(this.storage, this.usersApi);
    return new Application(usersRepository, timeSheetsRepository);
  }
}