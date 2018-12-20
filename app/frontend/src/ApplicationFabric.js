import UsersApi from "./api/usersApi";
import StorageAdapter from "./storage/StorageAdapter";
import UsersRepository from "./repositories/usersRepository";
import Application from "./Application";
import TimeSheetsApi from "./api/timeSheetsApi";
import TimeSheetsRepository from "./repositories/timeSheetsRepository";

export default class ApplicationFabric {
  createApplication() {
    this.usersApi = new UsersApi();
    this.timeSheetsApi = new TimeSheetsApi();
    this.storage = new StorageAdapter();

    const usersRepository = new UsersRepository(this.storage, this.usersApi);
    const timeSheetsRepository = new TimeSheetsRepository(this.storage, this.timeSheetsApi);
    return new Application(usersRepository, timeSheetsRepository);
  }
}