import React, {Component} from "react";
import NavBar from "./navbar/NavBar";

export default class BaseCabinetPage extends Component {
  renderContent = () => {
    throw new Error('You have to implement the method doSomething!');
  };

  render = () => {
    return (
      <div>
        <NavBar props={this.props}/>
        {this.renderContent()}
      </div>
    );
  }
}