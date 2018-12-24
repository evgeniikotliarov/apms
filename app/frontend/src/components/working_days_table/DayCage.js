export React, {Component} from 'react';
import './WorkingDaysTable.css';

export default class DayCage extends Component {
  render() {
    const {day} = this.props;
    return (
      <div>
        {day.day} --- {day.dayOfWeek}, {day.value}
      </div>
    );
  };
}