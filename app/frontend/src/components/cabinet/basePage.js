import React, {Component} from 'react';
import Navbar from "./navbar/Navbar";

export default class BaseCabinetPage extends Component {
  renderContent = () => {
    throw new Error('You have to implement the method doSomething');
  };

  render = () => {
    return(
      <div>
        <Navbar/>
        {this.renderContent()}
      </div>
    );
  }
}