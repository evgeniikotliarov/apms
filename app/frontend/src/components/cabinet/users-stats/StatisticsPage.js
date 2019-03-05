import React, {Component} from 'react';
import BaseCabinetPage from "../basePage";
import Application from "../../../Application";
import DateSlider from "../time-sheet/date-slider/DateSlider";
import StatisticsInfo from "./StatisticsInfo";

class StatisticsPage extends BaseCabinetPage {
  state = {
    timeSheet: []
  };

  fetchTimeSheets(date) {
    Application.timeSheetsUseCase.getTimeSheetsForDate(date)
      .subscribe(timeSheets => this.setState({timeSheets}))
  }

  renderContent = () => {
    return (
      <div className="statistic-page">
        <h1>Информация о рабочем времени пользователя</h1>
        <DateSlider handler={date => this.fetchTimeSheets(date)}/>
        <StatisticsInfo/>
      </div>
    )
  }
}
export default StatisticsPage;