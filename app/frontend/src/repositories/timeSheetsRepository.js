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
          this.saveTimeSheet(date);
          return data;
        }
      );
  };

  updateTimeSheetForDate = (date, sheet) => {
    const token = this.storage.loadData(TOKEN);
    const profileId = this.storage.loadData(PROFILE).id;
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.updateTimeSheet(token, profileId, year, month, sheet)
      .map(timeSheet => {
        this.saveTimeSheet(timeSheet);
        return timeSheet;
      });
  };

  updateOneDayOfTimeSheet = (timeSheetId, day, value) => {
    const token = this.storage.loadData(TOKEN);
    return this.api.updateOneDayOfTimeSheet(token, timeSheetId, day, value)
      .map(timeSheet => {
        this.saveTimeSheet(timeSheet);
        return timeSheet;
      });
  };

  getTimeSheetsForDate = (date) => {
    const token = this.storage.loadData(TOKEN);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    return this.api.getTimeSheets(token, year, month)
      .map(timeSheets => {
          for (const timeSheet of timeSheets)
            this.saveTimeSheet(timeSheet);
          return timeSheets;
        }
      )
  };

  saveTimeSheet(timeSheet) {
    const loadedTimeSheets = this.storage.loadData(TIME_SHEETS);
    loadedTimeSheets[`${timeSheet.month}.${timeSheet.year}`] = timeSheet;
    this.storage.saveData(TIME_SHEETS, loadedTimeSheets);
  }
}