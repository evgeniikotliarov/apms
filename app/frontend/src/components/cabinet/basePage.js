import React, {Component} from "react";
import NavBar from "./navbar/NavBar";
import Modal from "../common/Modal"

export default class BaseCabinetPage extends Component {
  state = {
    needToShowModal: false,
    modalRender: null
  };

  showModal(modalRender) {
    this.setState({needToShowModal: true});
    this.setState({modalRender})
  }

  hideModal() {
    this.setState({needToShowModal: false});
  }

  renderContent = () => {
    throw new Error('You have to implement the method doSomething!');
  };

  render = () => {
    return (
      <div>
        <NavBar props={this.props}/>
        <Modal
          showModal={this.state.needToShowModal}
          renderContent={this.state.modalRender}/>
        {this.renderContent()}
      </div>
    );
  }
}