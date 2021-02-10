import React, { useEffect, useState, useContext } from "react";
import { Link } from "react-router-dom";
import { MovieContext } from "../MovieContext";
import axios from "axios";
import urls from "../apiEndPoints";
import { GoPrimitiveDot } from "react-icons/go";
import { FaStar, FaPlus, FaPlay } from "react-icons/fa";
 
// Import styles
import Slider from "react-slick";
import "../styles/TestBanner.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

// Helper Component
const Details = ({ year, genre, time, review, movieName, desc, link }) => {
  const [appState] = useContext(MovieContext);
  function AddList() {
    axios
      .post(`https://movie-stream-api.herokuapp.com/api/add/list/${link}`)
      .then(res => console.log(res))
      .catch(err => console.log(err));
  }

  const detailStyle = {
    "backgroundImage": `url("https://res.cloudinary.com/du05mneox/image/upload/${movieName}.jpg")`,
    "opacity": appState.friendsDisplay ? "0.4" : "1",
  }
  return (
    <div className="details" style={detailStyle}>
      <div className="main-details">
        <p>Details: {(new Date(year)).getFullYear()} <GoPrimitiveDot size={13} /> <span className="genre">{genre}</span> <GoPrimitiveDot size={13} /> {Math.floor(time/60)}h {Math.floor(time % 60)}m</p>
        <p>Reviews: <span className="genre">IMDB</span> <GoPrimitiveDot size={13} /> {review}/10 <GoPrimitiveDot size={13} /> User rating <FaStar color="yellow" size={20} id="star" /> </p>
        <h3 className="title">{movieName}</h3>
        <p className="desc">{desc}</p>
        <div className="buttons">
          <Link 
            to={{ pathname: `/watch/${link}/`, state: { u_id: link, name: movieName }}}
            >
            <button className="watch-btn">
              <FaPlay id="watch-icon" className="icon" /> Watch
            </button>
          </Link>
          <Link to={`/#`}><button className="addlist" onClick={AddList}> <FaPlus id="add-icon" className="icon" /> Add List</button></Link>
        </div>
      </div>
    </div>
  )
};

export default function Banner() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    axios.get(urls.trending)
      .then(res => {
        setMovies(res.data.data.slice(0, 3));
      })
      .catch(error => console.log(error));
  }, [setMovies]);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    autoplaySpeed: 3000,
    autoplay: true,
    slidesToShow: 1,
    slidesToScroll: 1
  };  

  return (
    <div>
      <Slider {...settings}>
        {movies.map((movie, idx) => {
          // console.log(movie);
          return <Details year={movie.created_on} genre={movie.genre} time={movie.runtime} desc={movie.description} movieName={movie.name} key={`movie-${idx}`} review={movie.review} link={movie.public_id} />
        })}
      </Slider>
    </div>
  );
}
