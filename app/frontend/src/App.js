import React, {Component} from 'react';
import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import Login from "./components/login/Login";
import Signup from "./components/signup/Signup";
import NavbarEmployee from "./components/navbar/Navbar";
import NotFound from "./components/not_found/NotFound";

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      redirect: false

    };
  }

  render = () => {
    return (
      <Router>
        <div>
          <Route exact path="/login" component={(props) => <Login {...props}/>}/>
          <Route exact path="/signup" component={(props) => <Signup {...props}/>}/>
          <Route exact path="/" component={(props) => this.renderNavbar(props)}/>
          <Route exact path="*" component={(props) => <NotFound {...props}/>}/>
        </div>
      </Router>
    );
  };

}

export default App;
