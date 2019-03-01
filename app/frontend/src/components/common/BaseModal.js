import React, {Component} from 'react';
import './Modal.css';


class BaseModal extends Component {
  state = {
    closed: false
  };

  close() {
    this.setState({closed: true});
  }

  // noinspection JSMethodCanBeStatic
  head() {
    return null;
  }

  // noinspection JSMethodCanBeStatic
  content() {
    return null;
  }

  // noinspection JSMethodCanBeStatic
  foot() {
    return null;
  }

  render = () => {
    const display = this.props.showModal && !this.state.closed;
    this.state.closed = false;

    return display ? (
      <div className="modal">
        <div className="modal-content">
          <div className="modal-head">
            {this.head()}
          </div>
          <div className="modal-body">
            {this.content()}
          </div>
          <div className="modal-foot">
            {this.foot()}
          </div>
        </div>
      </div>
    ) : null
  }
}

export default BaseModal;