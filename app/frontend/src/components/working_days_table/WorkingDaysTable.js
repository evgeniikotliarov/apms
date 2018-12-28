import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";
import DayCage from "./DayCage";
import DateSlider from "../date-slider/DateSlider";

export default class WorkingDaysTable extends Component {
  componentWillMount() {
    Application.timeSheetsUseCase.getTimeSheetForCurrentDate()
      .subscribe(timeSheet => {
        this.setState({timeSheetId: timeSheet.id});
        this.setState({tableSheets: timeSheet.sheetsDay});
      });
  }

  state = {
    timeSheetId: '',
    tableSheets: []
  };

  render = () => {
    return (
      <div>
        <div className="date">
          <DateSlider/>
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