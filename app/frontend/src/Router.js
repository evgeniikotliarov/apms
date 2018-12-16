import React from 'react';
import {BroserRouter, Route} from 'react-router-dom';
import Login from "./components/login/Login";
import Signup from "./components/signup/Signup";
import NotFound from "./components/not_found/NotFound";
import Profile from "./components/profile/Profile";


class Router {
  static create() {
    return (<BrouserRouter>
      <div>
        <Route exact path="/" component={(props) => <Login {...props}/>}/>
        <Route exact path="/sign-up" component={(props) => <Signup {...props}/>}/>
        <Route exact path="/profile" component={(props) => <Profile {...props}/>}/>
        <Route exact path="*" component={(props) => <NotFound {...props}/>}/>
      </div>
    </BrouserRouter>)
  }
}

export default Router;