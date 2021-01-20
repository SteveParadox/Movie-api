import React, { useContext } from "react";
import "../styles/SubscribeLayout.css";
// import Carousel from 'react-elastic-carousel';
import Slider from "react-slick";
import { MovieContext } from "../MovieContext";
// import Item from "./Item2";
import Joker from "../joker_movie.jpg";
import MovieRating from "./MovieRating";
import { FaArrowRight } from "react-icons/fa"

const SlideShow = () => {
    const settings = {
        infinite: true,
        enableAutoPlay: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1
      };
      return (
        <div>
          <Slider {...settings}>
            <div className="Items">
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
            </div>
            <div className="Items">
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
            </div>
            <div className="Items">
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
            </div>
            <div className="Items">
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
            </div>
            <div className="Items">
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
              <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
            </div>
          </Slider>
        </div>
      );
}

const SubscribeLayout = () => {
    const {appState, setAppState} = useContext(MovieContext);

    return (
        <div className="subscribelayout">
            <div className="form-part">
                <div>
                    <h3 id="subscribe-tag">Subscribe</h3>
                    <p>Stay up to date</p>
                    <div className="input-part">
                        <input type="text" placeholder="E-mail" name="email" id="email"/>
                        <FaArrowRight className="send" size={22} color="grey" />
                    </div>
                </div>
            </div>
            <div className="slide-part">
                <SlideShow />
            </div>
        </div>
    );
}

export default SubscribeLayout;