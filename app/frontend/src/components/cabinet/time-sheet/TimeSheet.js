import React from 'react';
import {withRouter} from 'react-router-dom';
import './TimeSheet';
import BaseCabinetPage from "../basePage";
import WorkingDaysTable from "./workingDaysTable/WorkingDaysTable";

class TimeSheet extends BaseCabinetPage {
  renderContent = () => {
    return (
      <div className="Profile">
        <WorkingDaysTable/>
      </div>
    )
  };
}

export default withRouter(TimeSheet);