export default class TimeSheetUseCase {
  constructor(controller, repository) {
    this.controller = controller;
    this.repository = repository;
  }

  getTimeSheetForCurrentDate() {
    return this.repository.getTimeSheetForCurrentDate()
      .map(timeSheets => {
        const timeSheet = timeSheets[0];
        if (timeSheet === undefined) return;
        timeSheet['sheetsDay'] = this.controller.createBySheet(new Date(), timeSheet.sheet);
        return timeSheet;
      })
  }

  getTimeSheetForDate(date) {
    return this.repository.getTimeSheetForDate(date)
      .map(timeSheets => {
        const timeSheet = timeSheets[0];
        console.log(timeSheet, 'asdasd');
        timeSheet['sheetsDay'] = this.controller.createBySheet(date, timeSheet.sheet);
        return timeSheet;
      })
  }

  getTimeSheetsForDate(date) {
    return this.repository.getTimeSheetsForDate(date)
      .map(timeSheets => {
        for (const timeSheet of timeSheets) { // noinspection JSUnfilteredForInLoop
          timeSheet['sheetsDay'] = this.controller.createBySheet(date, timeSheet.sheet);
        }
        return timeSheets;
      })
  }

  updateOneDayOfTimeSheet(timeSheetId, day, value) {
    return this.repository.updateOneDayOfTimeSheet(timeSheetId, day, value)
      .map(timeSheet => {
          const date = new Date(timeSheet.year, timeSheet.month - 1, 1);
          timeSheet.sheetsDay = this.controller.createBySheet(date, timeSheet.sheet);
          return timeSheet;
        }
      );
  }
}