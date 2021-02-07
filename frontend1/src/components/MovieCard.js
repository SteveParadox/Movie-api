import React from "react";
import "../styles/MovieCard.css";
import Joker from "../joker_movie.jpg";
import { FaHeart, FaEye } from "react-icons/fa";

const ThreePic = () => {
  return (
    <div className="threepic">
      <img src={Joker} alt="t1"/>
      <img src={Joker} alt="t1"/>
      <img src={Joker} alt="t1"/>
    </div>
  );
};

const MovieCard = ({ title, like, viewed, friends, adPic }) => {
  // title -> the title of the movie
  // wish -> a boolean value to tell if movie is in wish list
  // viewed -> determines if you've seen the movie in this app before.
  // adPic => the picture to display in card background


  return (
    <div className="moviecard">
      <div>
        <img src={`https://res.cloudinary.com/du05mneox/image/upload/${title}.jpg`} alt="." id="adPic" />
        {/* <img src={Joker} alt="." id="adPic" /> */}
        <h3>{ title }</h3>
        <div className="end">
          <div className="picsOfFriends">
            <ThreePic /> 
          </div>
          <p>
            <FaHeart size={15} color={like ? "#2b2a30" : "var(--apps-red)"} />
            {" "}
            <FaEye size={15} color={viewed ? "var(--apps-red)" : "#2b2a30"} />
          </p>
        </div>
      </div>
    </div>
  );
};

export default MovieCard;