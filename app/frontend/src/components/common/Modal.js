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
    const display = this.props.showModal && !this.state.closed;
    this.state.closed = false;
    return display ? (
      <div className="modal">
        <div className="modal-content">
          <div className="modal-head">
            {this.props.renderHead()}
          </div>
          <div className="modal-body">
            {this.props.renderContent(() => this.close(this))}
          </div>
          <button onClick={event => this.onCloseModal(event)}>Отмена</button>
          <button className="save">Сохранить</button>
        </div>
      </div>
    ) : null
  }
}

export default Modal;