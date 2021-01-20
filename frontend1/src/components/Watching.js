// import React, { useContext } from "react";
import { FaAngleRight } from "react-icons/fa";
import "../styles/Watching.css";
import Joker from "../joker_movie.jpg";

const WatchCard = ({ thumbnail, title, perc }) => {
  // perc here refer to the point user stopped watching movie in percentage
  const cardStyle = {
    "backgroundImage": "url("+Joker+")",
  };
  const percStyle = {
    "width": perc + "%",
  };
  return (
    <div className="card" style={cardStyle}>
      <div className="details">
        <p className="title">{ title }</p>
        <div className="percentage">
          <div className="value" style={percStyle}></div>
        </div>
      </div>
    </div>
  );
}

const Watching = () => {
  return (
    <div className="watching">
      <div className="top">
        <p className="continue">Continue watching</p>
        <div className="filter">
          <p className="active">Recent</p>
          <p>Finished</p>
        </div>
        <div className="history">
          <p>View all history</p>
          <FaAngleRight size={22} color="grey" />
        </div>
      </div>
      <div className="cards">
        <WatchCard thumbnail={Joker} title="Onward" perc={40} />
        <WatchCard thumbnail={Joker} title="Onward" perc={40} />
        <WatchCard thumbnail={Joker} title="Onward" perc={40} />
        <WatchCard thumbnail={Joker} title="Onward" perc={40} />
      </div>
      <div className="history">
          <p>View all history</p>
          <FaAngleRight size={22} color="grey" />
        </div>
    </div>
  );
}

export default Watching;