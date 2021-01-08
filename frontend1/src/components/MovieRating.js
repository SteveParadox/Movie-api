import React from "react";

const MovieRating = ({ avatar, name, title, detail, rating }) => {
  return (
    <div className="rating">
      <div>
        <img src={avatar} alt="." className="avatar" />
        <h3>{name}</h3>
      </div>
      <div>
        <div className="movie-top">
          <p className="movie-title">{title}</p>
          <p className="movie-rating">🌟{rating}/10</p>
        </div>
        <p>{detail}</p>
      </div>
    </div>
  );
}

export default MovieRating;