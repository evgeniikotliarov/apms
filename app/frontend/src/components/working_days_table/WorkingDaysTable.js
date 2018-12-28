import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";
import DayCage from "./DayCage";
import DateSlider from "../date-slider/DateSlider";

export default class WorkingDaysTable extends Component {
  state = {
    timeSheetId: '',
    tableSheets: [],
    date: new Date()
  };

  componentWillMount() {
    this.handleFetchTimeSheet(this.state.date);
  }

  handleFetchTimeSheet = (date) => {
    Application.timeSheetsUseCase.getTimeSheetForDate(date)
      .subscribe(timeSheet => {
        if (timeSheet === undefined) {
          return;
        }
        console.log(timeSheet);
        //TODO fixed timesheet
        this.setState({date});
        this.setState({timeSheetId: timeSheet.id});
        this.setState({tableSheets: timeSheet.sheetsDay});
      });
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
      </div>
    )
  };

  renderCages() {
    return this.state.tableSheets.map((day, index) => {
      return (
        <div className="body" key={index}>
          <div className="table">
            <div>
              <DayCage day={day} timeSheetId={this.state.timeSheetId}/>
            </div>
          </div>
        </div>)
    })
  };
}