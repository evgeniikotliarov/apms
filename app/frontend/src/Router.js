import React from 'react';
import {BrowserRouter, Route} from 'react-router-dom';
import NotFound from "./components/not-found/NotFound";
import Login from "./components/login/Login";
import SignUp from "./components/signup/Signup";
import TimeSheet from "./components/cabinet/time-sheet/TimeSheet";
import UsersPage from "./components/cabinet/users/Users";
import Logout from "./components/cabinet/navbar/Logout";
import ProfilePage from "./components/cabinet/profile/ProfilePage";
import StatisticPage from "./components/cabinet/users-stats/StatisticsPage";

class Router {
  static create() {
    return (<BrowserRouter>
      <div>
        <Route exact path="/" component={(props) => <Login {...props}/>}/>
        <Route exact path="/log-out" component={(props) => <Logout {...props}/>}/>
        <Route exact path="/log-in" component={(props) => <Login {...props}/>}/>
        <Route exact path="/sign-up" component={(props) => <SignUp {...props}/>}/>
        <Route exact path="/time-sheet" component={(props) => <TimeSheet {...props}/>}/>
        <Route exact path="/profile" component={(props) => <ProfilePage {...props}/>}/>
        <Route exact path="/users" component={(props) => <UsersPage {...props}/>}/>
        <Route exact path="/statistics" component={(props) => <StatisticPage {...props}/>}/>
        <Route path="*" component={(props) => <NotFound {...props} />}/>
      </div>
    </BrowserRouter>)
  }
}

export default Router;
