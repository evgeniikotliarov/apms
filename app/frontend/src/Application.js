import React from 'react';
import ReactDOM from 'react-dom';
import Router from './Router'
import './Application.css';
import UsersApi from "./api/usersApi";

class App {
  constructor() {
    this.usersApi = new UsersApi();
  }

  run = () => {
    this.router = Router.create();
    this.render();
  };

  render = () => {
    return ReactDOM.render((
        <div className="container">
          <div className="row">
            {this.router}
          </div>
        </div>
      ),
      document.getElementById('root')
    );
  };
}

export default App;
