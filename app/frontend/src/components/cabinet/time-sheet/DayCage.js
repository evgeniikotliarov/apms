import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../../Application";
import DateConstants from "../../../domain/Constants"


export default class DayCage extends Component {
  COLORS = {
    0: '#ffd6cc',
    0.5: '#ffffb3',
    1: '#d9ffcc',
    weekend: '#dedede',
    workday: '#ddd',
    default: '#999'
  };

  getBackground = (day) => {
    const isNotWorkedWeekend = DateConstants.WEEKENDS.includes(day.dayOfWeek) && day.value === 0;
    if (isNotWorkedWeekend) return this.COLORS.weekend;
    else return this.COLORS[day.value];
  };

  handleUpdateDay(event) {
    const value = event.target.value;
    const timeSheetId = this.props.timeSheetId;
    const day = this.props.day.day;
    Application.timeSheetsUseCase.updateOneDayOfTimeSheet(timeSheetId, day, value)
      .subscribe(timeSheet => {
        this.setState({value});
        this.setState({color: this.COLORS[value]});
        this.props.handler(timeSheet);
      });
  }

  render() {
    const day = this.props.day;
    const color = this.getBackground(day);
    const style = {backgroundColor: color};
    return (
      <div style={style}>
        <p>{day.dayOfWeek}</p>
        <p><b>
          {day.day}
        </b></p>
        <select value={day.value}
                onChange={(event) => this.handleUpdateDay(event)}>
          <option>0</option>
          <option>0.5</option>
          <option>1</option>
        </select>
      </div>
    );
  };
}