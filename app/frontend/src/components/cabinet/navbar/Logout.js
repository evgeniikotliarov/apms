import React, {Component} from 'react';

const Logout = props => {
  return <a href="#" id="logout" className="log-out"
            onClick={props.handleLogout}>Log out</a>
};

export default Logout;