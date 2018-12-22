import React from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import Application from "../../../Application";
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "../../working_days_table/WorkingDaysTable";

class UserPage extends BaseCabinetPage {
  constructor() {
    super();
    this.fetchProfile();
    this.state = {
      name: null
    };
  }

  renderContent = () => {
    return (
      <div className="Profile">
        <WorkingDaysTable/>
        <h1 className="h1-user">User page</h1>
        <h1 className="name"> {this.state.name} </h1>
      </div>
    )
  };

  fetchProfile = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({name: profile.name});
      });
  }
}

export default withRouter(UserPage);