import React from 'react';
import './NotFound.css';

const pathNames = ['/', '/login', '/signup'];

const NotFound = props => {
  const checkPath = pathNames.indexOf(props.location.pathname);
  if (checkPath >= 0) {
    return null;
  }else {
    return (
      <div className="notFound">
        <h3 className="notfound-h3">404 page not found</h3>
        <h3 className="notfound-p">Страница не найдена</h3>
      </div>
    )
  }
};