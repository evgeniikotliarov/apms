import React from 'react';
import './Navbar.css';

export default function Navbar(props) {
  return(
    <div className="Navbar">
      <ul className="ul">
        <li className="li"><a href="#">My statistic</a></li>
        <li className="li"><a href="#">Other</a></li>
      </ul>
    </div>
  )
}