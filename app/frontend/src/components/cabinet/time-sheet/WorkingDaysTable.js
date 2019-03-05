import React, {Component} from 'react';
import './WorkingDaysTable.css';
import DayCage from "./DayCage";

export default class WorkingDaysTable extends Component {
  render = () => {
    return (
      <div>
        {this.renderCages()}
      </div>
    )
  };

  renderCages() {
    const timeSheet = this.props.timeSheet;
    return timeSheet? timeSheet.sheetsDay.map((day, index) => {
      // noinspection JSUnresolvedFunction
      return (
        <div className="body" key={index}>
          <div className="table">
            <div>
              <DayCage day={day}
                       timeSheetId={timeSheet.id}
                       updateTimeSheet={timeSheet => this.props.updateTimeSheet(timeSheet)}
              />
            </div>
          </div>
        </div>)
    }) : (<p>Loading ...</p>)
  };
}