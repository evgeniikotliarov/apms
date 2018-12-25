import React from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import Application from "../../../Application";
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "../../working_days_table/WorkingDaysTable";
import UserStats from "../../userStats/userStats";

class UserPage extends BaseCabinetPage {
  state = {
    name: null
  };

  componentWillMount = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({name: profile.name});
      });
  };

  renderContent = () => {
    return (
      <div className="Profile">
        <h1 className="h1-user">User page</h1>
        <h1 className="name"> {this.state.name} </h1>
        <WorkingDaysTable />
        <UserStats />
      </div>
    )
  };
}

export default withRouter(UserPage);