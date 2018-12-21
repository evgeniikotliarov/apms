export default class TimeSheetProvider {
  createEmpty = (date) => {
    const timeSheet = [];
    const daysInMonth = this.daysInMonth(date.getFullYear(), date.getMonth());
    for (let day = 1; day <= daysInMonth; day++) {
      const dayOfWeek = this.getDayOfWeek(date.getFullYear(), date.getMonth(), day);
      const sheetDay = {
        day: day, dayOfWeek: dayOfWeek, value: 0
      };
      timeSheet.push(sheetDay);
    }
    return timeSheet;
  };

  createBySheet = (date, sheet) => {
    const timeSheet = [];
    const daysInMonth = this.daysInMonth(date.getFullYear(), date.getMonth());
    for (let day = 1; day <= daysInMonth; day++) {
      const dayOfWeek = this.getDayOfWeek(date.getFullYear(), date.getMonth(), day);
      const sheetDay = {
        day: day, dayOfWeek: dayOfWeek, value: sheet[day - 1]
      };
      timeSheet.push(sheetDay);
    }
    return timeSheet;
  };

  getByTimeSheet = (timeSheet) => {
    const sheet = [];
    return sheet;
  };

  daysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  getDayOfWeek = (year, month, day) => {
    const textDayInWeek = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];
    const dayWeek = new Date(year, month, day).getDay();
    const dayOfWeek = textDayInWeek[dayWeek];
    return dayOfWeek;
  }
}