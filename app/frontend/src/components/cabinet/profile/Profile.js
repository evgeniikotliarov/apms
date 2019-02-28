import React from 'react';
import {withRouter} from 'react-router-dom';
import './Profile.css';
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "./workingDaysTable/WorkingDaysTable";

class UserPage extends BaseCabinetPage {
  renderContent = () => {
    return (
      <div className="Profile">
        <WorkingDaysTable/>
      </div>
    )
  };
}

export default withRouter(UserPage);