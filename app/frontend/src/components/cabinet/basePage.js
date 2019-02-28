import React, {Component} from "react";
import NavBar from "./navbar/NavBar";
import Modal from "../common/Modal";

export default class BaseCabinetPage extends Component {
  state = {
    needToShowModal: false,
    modalRenderHead: null,
    modalRenderContent: null
  };

  showModal(modalRenderHead, modalRenderContent) {
    this.setState({needToShowModal: true});
    this.setState({modalRenderHead: modalRenderHead});
    this.setState({modalRenderContent: modalRenderContent});
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
          renderHead={this.state.modalRenderHead}
          renderContent={this.state.modalRenderContent}/>
        {this.renderContent()}
      </div>
    );
  }
}