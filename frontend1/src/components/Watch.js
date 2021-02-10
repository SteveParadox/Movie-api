import React, { useState, useEffect } from "react";
import "../styles/Watch.css";
import AppNavBar from "./AppNavBar";
import SubcribeLayout from "./SubscribeLayout";
import Footer from "./Footer";
import Joker from "../joker_movie.jpg";
import MovieCard from "./MovieCard";
import ReactPlayer from "react-player";
import { FaEye, FaHeart, FaPlus, FaStar } from "react-icons/fa";
// import { MdPlaylistAdd } from "react-icons/md";


import axios from "axios";
// import { GoPrimitiveDot } from "react-icons/go";
// import urls from "../apiEndPoints";

/* Some small components */
// const Cast = ({ pic, actorName, name }) => {
//   return (
//     <div className="cast-item">
//       <img src={pic} alt="." />
//       <div>
//         <p>{actorName}</p>
//         <p>{name}</p>
//       </div>
//     </div>
//   );
// };

// const Friend = ({ pic, name, address }) => {
//   return (
//     <div className="friend">
//       <img src={pic} alt="." />
//       <div className="detail">
//         <h3>{name}</h3>
//         <p>{address}</p>
//       </div>
//     </div>
//   );
// };

const SimilarMovies = ({ u_id }) => {
  // fetch data from api using u_id
  const [movies, setMovies] = useState([]);
  useEffect(() => {
    const GetSimilarMovies = async (u_id) => {
      let similarMovies = [];
      try {
        const res = await axios.get(
          `https://movie-stream-api.herokuapp.com/api/similar/movie/${u_id}`
        );
        console.log(res);
        // set the value of similarMovies variable to the response
        setMovies(similarMovies);
      } catch (err) {
        console.log(err);
      }
    };
    GetSimilarMovies();
  }, [movies, u_id]);

  return (
    <div className="recommended">
      <p className="title">You might also like</p>
      <div className="show">
        {/* <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        />
        <MovieCard
          title="The Lord"
          liked={false}
          viewed={false}
          adPic={Joker}
        /> */}
        {movies.map((i, idx) => <MovieCard title={i.title} liked={i.liked} viewed={i.viewed} />)}
      </div>
    </div>
  );
};

const Watch = (props) => {
  const { match, location } = props;
  // console.log(match.params.movie_id);
  const u_id = match.params.movie_id;
  const movie_name = location.state.name;
  // const [data, setData] = useState({});
  // useEffect(() => {
  //   function fetchDetail() {
  //     axios.get(`https://movie-stream-api.herokuapp.com/api/get/movie/${u_id}/`)
  //       .then(res => console.log(res))
  //       .catch(err => console.log("Sorry, can't fetch movie detail!"));
  //   }
  //   fetchDetail();
  // }, []);
  return (
    <div className="watch">
      {/* {
        !data.logged_in ? <Redirect to="/signin" /> : null
      } */}
      <AppNavBar />
      <div className="watch-body">
        <div className="movieShow">
          <div className="vid">
            <div className="main">
              {/* <ReactPlayer 
                // url="http://filba.com/vid.mp4"
                url="http://192.168.43.157/vid.mp4"
                lazy="true"
                
                controls
                className="theShow"
              /> */}
              <video 
                poster={`https://res.cloudinary.com/du05mneox/video/upload/${movie_name}.jpg`}
                autoPlay={true}
                controls={true}
                className="theShow"
              >
                <source src={`https://res.cloudinary.com/du05mneox/video/upload/${movie_name}`} type="video/webm"/>
                <source src={`https://res.cloudinary.com/du05mneox/video/upload/${movie_name}`} type="video/mp4"/>
                <source src={`https://res.cloudinary.com/du05mneox/video/upload/${movie_name}`} type="video/ogg"/>
              </video>
            </div>
            <div className="actions">
              <p className="title">{movie_name}</p>
              <div className="btns">
                <div>
                  <FaHeart className="icons" /> <br />
                  <span>10 Likes</span>
                </div>
                <div>
                  <FaEye className="icons" /> <br />
                  <span>60m Views</span>
                </div>
                <div>
                  <FaPlus className="icons" /> <br />
                  <span>Add to list</span>
                </div>
              </div>
            </div>
            <div className="ratings">
                <p>Rating</p>
                <div className="stars">
                  <FaStar color="yellow"/>
                  <FaStar color="yellow"/>
                  <FaStar color="yellow"/>
                  <FaStar />
                  <FaStar />
                </div>
              </div>
          </div>
        </div>
        <div className="others">
          {/* <div className="cast">
            <h3 className="title">Cast</h3>
            <div className="display">
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
              <Cast pic={Joker} actorName="Elizabeth Debicki" name="Kat" />
            </div>
            <p>See More...</p>
          </div> */}
          {/* <div className="friends">
            <p className="title">Friends</p>
              <div className="show">
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <Friend pic={Joker} name="Justin Tik" address="@justti" />
                <p>See More..</p>
              </div>
          </div> */}
        </div>
        <SimilarMovies u_id={u_id} />
      </div>
      <SubcribeLayout />
      <Footer />
    </div>
  );
};

export default Watch;
