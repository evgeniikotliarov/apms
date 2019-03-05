import React from 'react';
import {withRouter} from 'react-router-dom';
import './TimeSheetPage';
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "./WorkingDaysTable";
import Application from "../../../Application";
import DateSlider from "../../common/DateSlider";
import UserStats from "./UserStats";

class TimeSheetPage extends BaseCabinetPage {
  state = {
    timeSheet: undefined
  };

  fetchTimeSheet = (date) => {
    Application.timeSheetsUseCase.getTimeSheetForDate(date)
      .subscribe(timeSheet => this.updateTimeSheet(timeSheet));
  };

  updateTimeSheet(timeSheet) {
    this.setState({timeSheet});
  }

  renderContent = () => {
    return (
      <div className="Profile">
        <div className="date panel-header">
          <DateSlider handler={date => this.fetchTimeSheet(date)}/>
        </div>
        <div className="sheet panel-body">
          <WorkingDaysTable
            timeSheet={this.state.timeSheet}
            updateTimeSheet={timeSheet => this.updateTimeSheet(timeSheet)}
          />
        </div>
        <UserStats timeSheet={this.state.timeSheet}/>
      </div>
    )
  };
}

export default withRouter(TimeSheetPage);