import React, { useContext } from "react";
import "../styles/SubscribeLayout.css";
import Carousel from 'react-elastic-carousel'
import { MovieContext } from "../MovieContext";
import Item from "./Item2";
import Joker from "../joker_movie.jpg";
import MovieRating from "./MovieRating";
import { FaArrowRight } from "react-icons/fa"

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
            <Carousel 
              itemsToShow={1}
              className="carousel-container"
              enableAutoPlay={true} 
              pagination={false}
            >
                <Item>
                    <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                    <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                </Item>
                <Item>
                <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                    <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                </Item>
                <Item>
                  <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                    <MovieRating avatar={Joker} name={"Sharon"} title={"The Avengers End Game"} detail={"lorem isp dum text that i kwek nwanwe a dey for you"} rating={8} />
                </Item>
            </Carousel>
            </div>
        </div>
    );
}

export default SubscribeLayout;