import React, { useContext } from "react";
import MovieCard from "./MovieCard";
import "../styles/MovieCard.css";
import { FaPlus, FaStar, FaFilm, FaFire } from "react-icons/fa";
import { BiTrendingUp } from "react-icons/bi";
import { GiAerialSignal } from "react-icons/gi";
import { MdMovie } from "react-icons/md";
import "../styles/Movies.css";

// Import slider and related stuff
import Slider from "react-slick";
import "../styles/TestBanner.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const PlusMovies = () => {
  return (
    <div className="plus-area">
      <div className="plus">
        <FaPlus size={28} color="grey" />
      </div>
    </div>
  );
};

const Category = ({title, icon}) => {
  return (
    <div className="category">
      {title}
    </div>
  );
};

const MovieDetails = (props) => {
  return (
    <div className="details">
      <p>{props.title}</p>
      <p>{props.details}</p>
    </div>
  );
}

const Movies = () => {
  const showDetails = () => {
    console.log("this");
  }
  const settings = {
    dots: false,
    lazyLoad: "ondemand",
    rtl: true,
    arrows: true,
    infinite: true,
    speed: 500,
    slidesToShow: 6,
    slidesToScroll: 3,
    mobileFirst: true,
    touchMove: true,
    responsive: [
      {
        breakpoint: 1240,
        settings: {
          slidesToShow: 4,
          slideToScroll: 2,
        }
      },
      {
        breakpoint: 930,
        settings: {
          slidesToShow: 3.4,
          slideToScroll: 1
        }
      },
      {
        breakpoint: 760,
        settings: {
          slidesToShow: 3
        }
      },
    ]
  };


  return (
    <div className="movies">

      <div className="top">
        <h3 className="active"> <MdMovie /> Movies</h3>
        <h3> <FaFilm /> Series</h3>
        <h3> <GiAerialSignal /> Live Streams</h3>
        <h3> <FaStar /> Premieres</h3>
      </div>

      <div className="genres">
      <Slider {...settings}>
        <Category title="Trending" icon={BiTrendingUp} />
        <Category title="Popular" icon={FaFire} />
        <Category title="Premieres" icon={FaStar} />
        <Category title="Popular" />
        <Category title="Popular" />

      </Slider>
      </div>

      <div className="sort">
        <div>
          Sort by: <select name="sortAlphabet" id="sortAlphabet">
            <option value="A-Z">A-Z</option>
            <option value="a-z">a-z</option>
            <option value="Z-A">Z-A</option>
            <option value="z-a">z-a</option>
          </select>
        </div>
        <div>
          <FaStar color="yellow" size={20} />
          <div className="progress">
            <div className="value"></div>
          </div>
          <span>7</span>
        </div>
      </div>
      <div className="displayMovies">
        <div>
          <MovieCard title="Stuff" like={true} viewed={true} onClick={showDetails}/>
        </div>
        <div>
          <MovieCard title="Stuff" like={true} viewed={true} onClick={showDetails} />
        </div>
        <div>
          <MovieCard title="Stuff" like={true} viewed={true} onClick={showDetails} />
        </div>
        <div>
          <MovieCard title="Stuff" like={true} viewed={true} onClick={showDetails} />
        </div>
        <div>
          <MovieCard title="Stuff" like={true} viewed={true} onClick={showDetails} />
        </div>
      </div>
      <PlusMovies />
    </div>
  );
}

export default Movies;