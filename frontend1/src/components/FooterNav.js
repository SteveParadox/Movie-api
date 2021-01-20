import React from 'react';
import { Link } from "react-router-dom";
import "../styles/FooterNav.css";

const FooterNav = () => {
  return (
    <div className="footernav">
      <Link to="/home">
        <p>Home</p>
      </Link>
      <Link to="/movies">
        <p>Movies</p>
      </Link>
      <Link to="/series">
        <p>Series</p>
      </Link>
      <Link to="/live">
        <p>Live</p>
      </Link>
      <Link to="/list">
        <p>My list</p>
      </Link>
    </div>
  );
}

export default FooterNav;