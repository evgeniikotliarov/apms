import React, {Component} from 'react';
import './Modal.css';

export default class Modal extends Component {
  state = {
    closed: false
  };

  closeModal(event) {
    event.preventDefault();
    this.setState({closed: true})
  };

  render = () => {
    const display = this.props.showModal && !this.state.closed;
    this.state.closed = false;
    return display ? (
      <div className="modal">
        <div className="modal-head">
          <button onClick={event => this.closeModal(event)}><i className="material-icons">close</i></button>
        </div>
        <div className="modal-body">
          {this.props.renderContent()}
        </div>
        <button onClick={event => this.closeModal(event)}>Отмена</button>
        <button className="save">Сохранить</button>
      </div>
    ): null
  }
}