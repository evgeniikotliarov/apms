const TOKEN = 'token';
const PROFILE = 'profile';
const TIME_SHEETS = 'timeSheets';

export default class TimeSheetsRepository {
  constructor(storage, api) {
    this.storage = storage;
    this.api = api;
  }

  getTimeSheetForCurrentDate = () => {
    const now = new Date();
    return this.getTimeSheetForDate(now)
  };

  getTimeSheetForDate = (date) => {
    const token = this.storage.loadData(TOKEN);
    const profileId = this.storage.loadData(PROFILE).id;
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.getTimeSheet(token, profileId, year, month)
      .map(data => {
        const timeSheets = this.storage.loadData(TIME_SHEETS);
        timeSheets[`${month}.${year}`] = data;
        this.storage.saveData(TIME_SHEETS, timeSheets);
        return data
      }
    )
  };

  updateTimeSheetForDate = (date, sheet) => {
    const token = this.storage.loadData(TOKEN);
    const profileId = this.storage.loadData(PROFILE).id;
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.updateTimeSheet(token, profileId, year, month, sheet)
      .map(data => {
        const timeSheets = this.storage.loadData(TIME_SHEETS);
        timeSheets[`${month}.${year}`] = data;
        this.storage.saveData(TIME_SHEETS, timeSheets);
        return data
      }
    )
  };

  getTimeSheetsForDate = (date) => {
    const token = this.storage.loadData(TOKEN);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.getTimeSheets(token, year, month)
      .map(data => {
        const timeSheets = this.storage.loadData(TIME_SHEETS);
        for (const timeSheet in data)
          timeSheets[`${month}.${year}`] = data;
        this.storage.saveData(TIME_SHEETS, timeSheets);
        return data
      }
      )
  };
}