import React, { useContext } from "react";
import "../styles/Recommendations.css";
import MovieCard from "./MovieCard";
// import Carousel from "react-elastic-carousel";
import Joker from "../joker_movie.jpg";

// Import styles
import Slider from "react-slick";
import "../styles/TestBanner.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";



const Recommendations = (props) => {
  const settings = {
    dots: false,
    lazyLoad: "ondemand",
    arrows: true,
    infinite: true,
    speed: 500,
    slidesToShow: 5.4,
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
      {
        breakpoint: 660,
        settings: {
          slidesToShow: 2
        }
      },
      {
        breakpoint: 448,
        settings: {
          slidesToShow: 1
        }
      }
    ]
  };

  return (
    <div className="recommendations">
      <div className="top">
          <div className="title">Recommendations</div>
          <div className="filter">
            <p>Filba</p>
            <p className="active">Friends</p>
          </div>
      </div>
      <div className="top1">
        <p>Recommendations</p>
        <div className="filter">
            <p>Filba</p>
            <p className="active">Friends</p>
        </div>
      </div>

      {/* <button {...props} onClick={() => Slider.slickPrev()}>Prev</button> */}
      <Slider {...settings}>
        <MovieCard title="Old Guard" like={false} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={false} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={false} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={false} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
      </Slider>
      {/* <button {...props} onClick={() => Slider.slickNext()}>Next</button> */}
      {/* <Carousel
        itemsToShow={5.5}
        pagination={false}
        enableSwipe={true}
        style={{
          "padding": "20px"
        }}
      >
        <MovieCard title="Old Guard" like={false} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={false} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />
        <MovieCard title="Old Guard" like={true} viewed={true} adPic={Joker} />

      </Carousel> */}
    </div>
  );
}

export default Recommendations;