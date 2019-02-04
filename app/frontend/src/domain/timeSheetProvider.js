import DateConstants from "./Constants"
class TimeSheetProvider {
  textDayInWeek = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];

  createEmpty = (date) => {
    const timeSheet = [];
    const daysInMonth = this.daysInMonth(date.getFullYear(), date.getMonth());
    for (let day = 1; day <= daysInMonth; day++) {
      const dayOfWeek = this.getDayOfWeek(date.getFullYear(), date.getMonth(), day);
      const sheetDay = {day: day, dayOfWeek: dayOfWeek, value: 0};
      timeSheet.push(sheetDay)
    }
    return timeSheet;
  };

  createBySheet = (date, sheet) => {
    const timeSheet = [];
    const daysInMonth = this.daysInMonth(date.getFullYear(), date.getMonth());
    for (let day = 1; day <= daysInMonth; day++) {
      const dayOfWeek = this.getDayOfWeek(date.getFullYear(), date.getMonth(), day);
      const sheetDay = {day: day, dayOfWeek: dayOfWeek, value: sheet[day - 1]};
      timeSheet.push(sheetDay)
    }
    return timeSheet;
  };

  getByTimeSheet = (timeSheet) => {
    const sheet = [];
    for (const sheetDay in timeSheet) { // noinspection JSUnfilteredForInLoop
      sheet.push(sheetDay.value);
    }
    return sheet;
  };

  daysInMonth = (year, month) => {
    return new Date(year, month + 1 , 0).getDate();
  };

  getDayOfWeek = (year, month, day) => {
    const dayWeek = new Date(year, month, day).getDay();
    return DateConstants.TEXT_DAY_IN_WEEK[dayWeek];
  }
}

export default TimeSheetProvider;