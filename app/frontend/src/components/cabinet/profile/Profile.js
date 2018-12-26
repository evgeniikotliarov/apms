import React from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "../../working_days_table/WorkingDaysTable";
import UserStats from "../../userStats/userStats";

class UserPage extends BaseCabinetPage {

  renderContent = () => {
    return (
      <div className="Profile">
        <h1 className="h1-user">User page</h1>
        <WorkingDaysTable />
        <UserStats />
      </div>
    )
  };
}

export default withRouter(UserPage);