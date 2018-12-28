import React, {Component} from 'react';

class DateSlider extends Component {
  constructor() {
    super();
    const now = new Date();
    this.state = {
      currentDate: now
    };
    this.previousMonth = this.previousMonth.bind(this);
    this.nextMonth = this.nextMonth.bind(this);
  }

  allMonth = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
    "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

  previousMonth = () => {
    const currentDate = this.state.currentDate;
    const month = currentDate.getMonth();
    currentDate.setMonth(month - 1);
    this.setState({currentDate});
  };

  nextMonth = () => {
    if (this.state.currentDate.getMonth() === new Date().getMonth())
      return;
    const currentDate = this.state.currentDate;
    const month = currentDate.getMonth();
    currentDate.setMonth(month + 1);
    this.setState({currentDate});
  };

  render = () => {
    const stringMonth = this.allMonth[this.state.currentDate.getMonth()];
    const year = this.state.currentDate.getFullYear();
    return (
      <div className="date">
        <button className="button-arrow" onClick={this.previousMonth}>
          <i className="material-icons">keyboard_arrow_left</i>
        </button>
        <span>{stringMonth} {year}</span>
        <button className="button-arrow" onClick={this.nextMonth}>
          <i className="material-icons">keyboard_arrow_right</i>
        </button>
      </div>
    )
  };
}


export default DateSlider;