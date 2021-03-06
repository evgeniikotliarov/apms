import UsersApi from "./api/usersApi";
import StorageAdapter from "./storage/StorageAdapter";
import UsersRepository from "./repositories/usersRepository";
import Application from "./Application";
import TimeSheetsApi from "./api/timeSheetsApi";
import TimeSheetsRepository from "./repositories/timeSheetsRepository";
import UsersUseCase from "./useCases/userUseCases";
import TimeSheetUseCase from "./useCases/timeSheetUseCases";
import TimeSheetProvider from "./domain/timeSheetProvider";

export default class ApplicationFabric {
  createApplication() {
    const usersApi = new UsersApi();
    const timeSheetsApi = new TimeSheetsApi();
    const storage = new StorageAdapter();

    this.usersRepository = new UsersRepository(storage, usersApi);
    this.timeSheetsRepository = new TimeSheetsRepository(storage, timeSheetsApi);

    this.timeSheetsController = new TimeSheetProvider();

    const usersUseCase = new UsersUseCase(this.usersRepository);
    const timeSheetsUseCase = new TimeSheetUseCase(this.timeSheetsController, this.timeSheetsRepository);

    return new Application(usersUseCase, timeSheetsUseCase);
  }
}