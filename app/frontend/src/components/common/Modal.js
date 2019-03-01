import React, {Component} from 'react';
import './Modal.css';


class Modal extends Component {
  state = {
    closed: false
  };

  onCloseModal(event) {
    event.preventDefault();
    this.close();
  };

  close() {
    this.setState({closed: true});
  }

  render = () => {
    if (this.props.render === undefined) return null;

    const display = this.props.showModal && !this.state.closed;
    this.state.closed = false;
    this.props.render.setDialog(this);
    return display ? (
      <div className="modal">
        <div className="modal-content">
          <div className="modal-head">
            {this.props.render.head()}
          </div>
          <div className="modal-body">
            {this.props.render.content()}
          </div>
          <div className="modal-foot">
            {this.props.render.foot()}
          </div>
        </div>
      </div>
    ) : null
  }
}

export default Modal;