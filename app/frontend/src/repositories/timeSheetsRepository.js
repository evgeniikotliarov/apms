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
    return this.getTimeSheetForDate(now);
  };

  getTimeSheetForDate = (date) => {
    const token = this.storage.loadData(TOKEN);
    const profileId = this.storage.loadData(PROFILE).id;
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.getTimeSheet(token, profileId, year, month)
      .map(data => {
          this.saveTimeSheets(`${month}.${year}`, data);
          return data;
        }
      );
  };

  updateTimeSheetForDate = (date, sheet) => {
    const token = this.storage.loadData(TOKEN);
    const profileId = this.storage.loadData(PROFILE).id;
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    // noinspection JSUnusedLocalSymbols
    return this.api.updateTimeSheet(token, profileId, year, month, sheet)
      .map(response => {
        const loadedTimeSheets = this.storage.loadData(TIME_SHEETS);
        loadedTimeSheets[`${month}.${year}`].sheet = sheet;
        this.storage.saveData(TIME_SHEETS, loadedTimeSheets);
        return response;
      });
  };

  updateOneDayOfTimeSheet = (timeSheetId, day, value) => {
    const token = this.storage.loadData(TOKEN);
    return this.api.updateOneDayOfTimeSheet(token, timeSheetId, day, value)
      .map(status => {
        const loadedTimeSheets = this.storage.loadData(TIME_SHEETS);
        Object.entries(loadedTimeSheets, entry => {
          const key = entry[0];
          loadedTimeSheets[key].sheet[day - 1] = entry[1];
        });
        this.storage.saveData(TIME_SHEETS, loadedTimeSheets);
        return status;
      });
  };

  getTimeSheetsForDate = (date) => {
    const token = this.storage.loadData(TOKEN);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.getTimeSheets(token, year, month)
      .map(data => {
          this.saveTimeSheets(`${month}.${year}`, data);
          return data;
        }
      )
  };

  saveTimeSheets(name, timeSheets) {
    const loadedData = this.storage.loadData(TIME_SHEETS);
    const loadedTimeSheets = loadedData === null ? {} : loadedData;
    for (const timeSheet of timeSheets)
      loadedTimeSheets[name] = timeSheet;
    this.storage.saveData(TIME_SHEETS, loadedTimeSheets);
  }
}