export default class TimeSheetUseCase {
  constructor(controller, repository) {
    this.controller = controller;
    this.repository = repository;
  }

  getTimeSheetForCurrentDay() {
    return this.repository.getTimeSheetsForCurrentDate()
      .map(timeSheets => {
        const timeSheet = timeSheets[0];
        timeSheet['sheetsDay'] = this.controller.createBySheet(new Date(), timeSheet.sheet);
        return timeSheet;
      })
  }

  getTimeSheetsForCurrentDate(date) {
    return this.repository.getTimeSheetsForDate(date)
      .map(timeSheets => {
        for (const timeSheet of timeSheets) {
          timeSheet['sheetsDay'] = this.controller.createBySheet(date, timeSheet.sheet)
        }
        return timeSheets;
      })
  }
}