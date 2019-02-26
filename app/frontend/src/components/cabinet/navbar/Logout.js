import React, {Component} from 'react';

const Logout = props => {
  return <a href="/log-out" className="log-out"
            onClick={props.handleLogout}>Log out</a>
};

export default Logout;