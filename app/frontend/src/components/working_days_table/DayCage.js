import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";


export default class DayCage extends Component {
  COLORS = {
    0: '#e55',
    0.5: '#ee5',
    1: '#5e5',
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
    const timeSheetId = this.state.timeSheetId;
    const day = this.state.day;
    Application.timeSheetsUseCase.updateOneDayOfTimeSheet(timeSheetId, day, value)
      .subscribe(() => {
        this.setState({value});
        this.setState({color: this.COLORS[value]});
      });
  }

  render() {
    const {day} = this.props;
    const style = {backgroundColor: this.state.color};
    return (
      <div style={style}>
        <p>{day.dayOfWeek}</p>
        <p>
          {day.day}
        </p>
        <select value={this.state.value}
                onChange={(event) => this.handleUpdateDay(event)}>
          <option>0</option>
          <option>0.5</option>
          <option>1</option>
        </select>
      </div>
    );
  };
}