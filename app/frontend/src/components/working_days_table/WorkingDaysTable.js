import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";
import DayCage from "./DayCage";
import DateSlider from "../date_slider/DateSlider";
import UserStats from "../userStats/userStats";

export default class WorkingDaysTable extends Component {
  state = {
    timeSheet: null,
  };

  componentWillMount() {
    this.handleFetchTimeSheet(this.state.date);
  }

  handleFetchTimeSheet = (date) => {
    Application.timeSheetsUseCase.getTimeSheetForDate(date)
      .subscribe(timeSheet => {
        if(timeSheet === undefined) return;
        this.setState({date, timeSheet})
      });
  };

  handleUpdateTimeSheet = (timeSheet) => {
    this.setState({timeSheet})
  };

  render = () => {
    return (
      <div>
        <div className="date">
          <DateSlider handler={this.handleFetchTimeSheet}/>
        </div>
        <div className="dayCage">
          {this.renderCages()}
        </div>
        <UserStats timeSheet={this.state.timeSheet}/>
      </div>
    )
  };

  renderCages() {
    const timeSheet = this.state.timeSheet;
    if (timeSheet === null) return;
    return timeSheet.sheetsDay.map((day, index) => {
      return (
        <div className="body" key={index}>
          <div className="table">
            <div>
              <DayCage day={day}
                       timeSheetId={timeSheet.id}
                       handler={this.handleUpdateTimeSheet}
              />
            </div>
          </div>
        </div>)
    })
  };
}