import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";
import DayCage from "./DayCage";


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
    year: '',
    month: '',
    allMonth: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
      "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    tableSheets: []
  };

  render = () => {
    const currentDay = new Date();
    const year = currentDay.getFullYear();
    const month = currentDay.getMonth();
    const convertMonth = this.state.allMonth[month];


    return (
      <div>
        <div className="date">{convertMonth}-{year}</div>
        <div className="dayCage">
          {this.renderCages()}
        </div>
      </div>
    )
  };

  renderCages() {

    return this.state.tableSheets.map((day, index ) => {
      return (
        <div className="body" key={index}>
          <div className="table">
            <div>
              <DayCage day={day} timeSheetId={this.state.timeSheetId} />
            </div>
          </div>
        </div>)
    })
  };
}