import React, { useState, useEffect } from "react";
import "../styles/Watch.css";
import AppNavBar from "./AppNavBar";
import SubcribeLayout from "./SubscribeLayout";
import Footer from "./Footer";
import Joker from "../joker_movie.jpg";
import MovieCard from "./MovieCard";
import ReactPlayer from "react-player";
import { GetSimilarMovies } from "./Helper";
import { FaThumbsUp, FaThumbsDown, FaShareAlt, FaRegSave } from "react-icons/fa";

/* Some small components */
const Cast = ({ pic, actorName, name }) => {
  return (
    <div className="cast-item">
      <img src={pic} alt="." />
      <div>
        <p>{actorName}</p>
        <p>{name}</p>
      </div>
    </div>
  );
};

const Friend = ({ pic, name, address }) => {
  return (
    <div className="friend">
      <img src={pic} alt="." />
      <div className="detail">
        <h3>{name}</h3>
        <p>{address}</p>
      </div>
    </div>
  );
};

const SimilarMovies = ({ u_id }) => {
  // fetch data from api using u_id
  const [movies, setMovies] = useState([]);
  useEffect(() => {
    setMovies(GetSimilarMovies(u_id));
    console.log(movies);
  }, [movies, u_id]);

  return (
    <div className="recommended">
      <p className="title">Recommended</p>
      <div className="show">
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        {/* {movies.map((i, idx) => <MovieCard title={i.title} liked={i.liked} viewed={i.viewed} adPic={i.poster} />)} */}
      </div>
    </div>
  );
};

const Watch = ({ match }) => {
  console.log(match.params.movie_id);
  const u_id = match.params.movie_id;
  return (
    <div className="watch">
      <AppNavBar />
      <div className="watch-body">
        <div className="movieShow">
          <div className="vid">
            <ReactPlayer
              url={`https://movie-stream-api.herokuapp.com/api/get/movie/${u_id}/`}
              controls={true}
              width="100%"
              height="auto"
            />
            {/* <video
            src={`https://movie-stream-api.herokuapp.com/api/get/movie/${u_id}/`}
          ></video> */}
            <div className="vid-btns">
              <button>
                <FaThumbsUp color="var(--font-white)" /> <br/>
                Like
              </button>
              <button>
                <FaThumbsDown color="var(--font-white)" />
              </button>
              <button>
                <FaShareAlt color="var(--font-white)" />
              </button>
              <button>
                <FaRegSave color="var(--font-white)" />
              </button>
            </div>
          </div>
        </div>
        <div className="others">
          <div className="cast">
            <h3 className="title">Cast</h3>
            <div className="display">
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
            </div>
            <p>See More...</p>
          </div>
          <div className="friends">
            <div className="bordered">
              <div className="show">
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <p>See More..</p>
              </div>
            </div>
            <p className="title">Friends</p>
          </div>
        </div>
        <SimilarMovies u_id={u_id} />
      </div>
      <SubcribeLayout />
      <Footer />
    </div>
  );
};

export default Watch;
