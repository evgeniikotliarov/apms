import React from 'react';
import ReactDOM from 'react-dom';
import Router from './Router'
import './Application.css';

class Application {
  constructor(userRepository) {
    Application.userRepository = userRepository;
  }

  run = () => {
    this.render();
  };

  render = () => {
    return ReactDOM.render((
        <div className="container">
          <div className="row">
            {Router.create()}
          </div>
        </div>
      ),
      document.getElementById('root')
    );
  };
}

export default Application;
