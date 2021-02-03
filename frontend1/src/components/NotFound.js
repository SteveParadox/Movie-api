import React from "react";
import { Link } from "react-router-dom";
import NavBar from "./AppNavBar";
import "../styles/NotFound.css";
import Film from "../white-film.png";

const NotFound = ({ match }) => {
  return (
    <div className="notFoundPage">
      <NavBar />
      <div className="top">
        <h1 className="four">4</h1>
        <img src={Film} alt="0"/>
        <h1 className="four">4</h1>
      </div>
      <div className="info">Ooops! <span className="red-part">\{match.params.unknown}</span> not found - <Link to="/"><button className="home">Home</button></Link></div>
    </div>
  );
};

export default NotFound;