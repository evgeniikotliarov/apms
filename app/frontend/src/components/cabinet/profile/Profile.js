import React from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "../../workingDaysTable/WorkingDaysTable";

class UserPage extends BaseCabinetPage {
  renderContent = () => {
    return (
      <div className="Profile">
        <h1 className="h1-user">User page</h1>
        <WorkingDaysTable/>
      </div>
    )
  };
}

export default withRouter(UserPage);