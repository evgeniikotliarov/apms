import React, {Component} from 'react';
import DateConstants from "../../domain/Constants";

class DateSlider extends Component {
  state = {
    currentDate: new Date()
  };

  componentWillMount() {
    this.props.handler(this.state.currentDate);
  }

  previousMonth = () => {
    if (this.state.currentDate - 1 < DateConstants.FIXED_MINIMAL_DATE)
      return;
    const currentDate = this.state.currentDate;
    const month = currentDate.getMonth();
    currentDate.setMonth(month - 1);
    currentDate.setDate(1);
    this.setState({currentDate});
    this.props.handler(currentDate);
  };

  nextMonth = () => {
    if (this.state.currentDate.getMonth() === new Date().getMonth())
      return;
    const currentDate = this.state.currentDate;
    const month = currentDate.getMonth();
    currentDate.setMonth(month + 1);
    currentDate.setDate(1);
    this.setState({currentDate});
    this.props.handler(currentDate);
  };

  render = () => {
    const stringMonth = DateConstants.TEXT_MONTH[this.state.currentDate.getMonth()];
    const year = this.state.currentDate.getFullYear();
    return (
      <div className="date">
        <button className="button-arrow" onClick={() => this.previousMonth()}>
          <i className="material-icons">keyboard_arrow_left</i>
        </button>
        <span>{stringMonth} {year}</span>
        <button className="button-arrow" onClick={() => this.nextMonth()}>
          <i className="material-icons">keyboard_arrow_right</i>
        </button>
      </div>
    )
  };
}


export default DateSlider;