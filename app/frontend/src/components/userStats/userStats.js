import React, {Component} from 'react';
import Application from "../../Application";
import '../workingDaysTable/WorkingDaysTable.css'

class UserStats extends Component {
  state = {
    vacation: '',
    rate: '',
    employment_date: '',
    acceptance_date: '',
    activated: '',
    closed: '',
    norm: ''

  };

  componentWillMount() {
    Application.timeSheetsUseCase.getTimeSheetForCurrentDate()
      .subscribe(timeSheet => {
        this.setState({rate: timeSheet.rate});
        this.setState({closed: timeSheet.closed});
        this.setState({norm: timeSheet.norm});
      });
  };

  componentDidMount = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({vacation: profile.vacation});
        this.setState({employment_date: profile.employment_date});
        this.setState({acceptance_date: profile.acceptance_date});
        this.setState({activated: profile.activated});
      });
  };

  render() {
    return (
      <div className="userStats">
        <div>
          <p>Зачислено отпускных дней: <b>{this.state.vacation === null ? "0" : this.state.vacation }</b></p>
        </div>
        <div>
          <p>Тариф отпускных дней: <b>{this.state.rate}</b></p>
        </div>
        <div>
          <p>Дата приема: <b>{this.state.employment_date}</b></p>
        </div>
        <div>
          <p>Дата регистрации: <b>{this.state.acceptance_date}</b></p>
        </div>
        <div>
          <p>Активирован: <b>{this.state.activated === true ? "Да" : 'Нет'}</b></p>
        </div>
        <div>
          <p>Норма рабочих дней: <b>{this.state.norm}</b></p>
        </div>
        <div>
          <p>Закрыт период: <b>{this.state.closed === true ? "Да" : 'Нет'}</b></p>
        </div>
      </div>
    );
  }
}

export default UserStats;