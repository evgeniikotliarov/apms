import React, {Component} from 'react';
import './WorkingDaysTable.css';
import Application from "../../Application";
import DayCage from "./DayCage";


export default class WorkingDaysTable extends Component {
  constructor() {
    super();
    this.fetchTimeSheets();
  }

  fetchTimeSheets() {
    Application.timeSheetsUseCase.getTimeSheetForCurrentDate()
      .subscribe(timeSheet => {
        console.log(timeSheet);
        this.setState({tableSheets: timeSheet.sheetsDay});
      });
  }

  state = {
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
        <div className="table">
          {this.renderCages()}
        </div>
      </div>
    )
  };

  renderCages() {
    return this.state.tableSheets.map((day, index ) => {
      return (
        <div key={index}>
          <DayCage day={day} />
        </div>)
    })
  };
}