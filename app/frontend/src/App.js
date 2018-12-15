import React, {Component} from 'react';
import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import Login from "./components/login/Login";

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
        </div>
      </Router>
    );
  };

}

export default App;
