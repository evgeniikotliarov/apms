import React, {Component} from 'react';
import Application from "../../../Application";

class UserStats extends Component {
  constructor() {
    super();
    this.fetchProfile();
    this.state = {
      profile: null
    };
  }

  fetchProfile = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => this.setState({profile}))
  };

  render() {
    const {timeSheet} = this.props;
    const profile = this.state.profile;
    if (!timeSheet || !profile)
      return (<div className="userStats">loading</div>);
    return (
      <div className="userStats">
        <div>
          <p>Зачислено отпускных дней:
            <b>{timeSheet.vacation === null ? "0" : timeSheet.vacation}</b></p>
        </div>
        <div>
          <p>Тариф отпускных дней: <b>{timeSheet.rate}</b></p>
        </div>
        <div>
          <p>Дата приема: <b>{profile.employment_date}</b></p>
        </div>
        <div>
          <p>Дата регистрации: <b>{profile.acceptance_date}</b></p>
        </div>
        <div>
          <p>Активирован: <b>{profile.activated === true ? "Да" : 'Нет'}</b></p>
        </div>
        <div>
          <p>Норма рабочих дней: <b>{timeSheet.norm}</b></p>
        </div>
        <div>
          <p>Закрыт период: <b>{timeSheet.closed === true ? "Да" : 'Нет'}</b></p>
        </div>
      </div>
    );
  }
}

export default UserStats;