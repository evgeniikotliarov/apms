import React from 'react';
import './NotFound.css';

const pathNames = ["/", "/log-in", "/sign-up", "/profile", "/users"];

const NotFound = props => {
  const checkPath = pathNames.indexOf(props.location.pathname);
  if (checkPath >= 0) {
    return null;
  }else{
    return (
      <div className="notfound">
        <h3 className="notfound-h3">404 page not found</h3>
        <p className="notfound-p">Страница не найдена.</p>
      </div>)
  }
};

export default NotFound;