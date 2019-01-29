import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";


export default class DayCage extends Component {
  COLORS = {
    0: '#ffd6cc',
    0.5: '#ffffb3',
    1: '#d9ffcc',
    weekend: '#aaa',
    workday: '#ddd'
  };

  state = {
    timeSheetId: this.props.timeSheetId,
    day: this.props.day.day,
    dayOfWeek: this.props.day.dayOfWeek,
    value: this.props.day.value,
    color: this.COLORS[this.props.day.value]
  };

  handleUpdateDay(event) {
    const value = event.target.value;
    const timeSheetId = this.props.timeSheetId;
    const day = this.state.day;
    Application.timeSheetsUseCase.updateOneDayOfTimeSheet(timeSheetId, day, value)
      .subscribe(timeSheet => {
        this.setState({value});
        this.setState({color: this.COLORS[value]});
        this.props.handler(timeSheet);
      });
  }

  render() {
    const day = this.props.day;
    this.state.color = this.COLORS[day.value];
    const style = {backgroundColor: this.state.color};
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