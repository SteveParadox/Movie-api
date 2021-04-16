import React, { useState, useEffect } from "react";
import "../styles/Watch.css";
import AppNavBar from "./AppNavBar";
import SubcribeLayout from "./SubscribeLayout";
import Footer from "./Footer";
import Joker from "../joker_movie.jpg";
import MovieCard from "./MovieCard";
// import ReactPlayer from "react-player";
import { FaEye, FaHeart, FaPlus, FaStar, FaArrowLeft } from "react-icons/fa";
import logo from "../video-camera.svg";
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


const Watch = (props) => {
  const { match, location } = props;
  console.log("This is the movie_id: ", match.params.movie_id);
  const u_id = match.params.movie_id;
  // debugger;
  const [movie_name, setMovieName] = useState("");
  const [movie_id, setMovieId] = useState("");
  const [likes, setLikes] = useState(0);
	const [views, setViews] = useState(0);
	const [showFriends, setShowFriends] = useState(true);
	const [showChat, setShowChat] = useState(false);
  // const [data, setData] = useState({});
  useEffect(() => {
    function fetchDetail() {
      axios.post(`https://movie-stream-api.herokuapp.com/api/get/movie/${u_id}/`, {
        "token": localStorage.getItem("token"),
      })
        .then(res => {
          console.log(res.data);
          setMovieName(res.data.data.name);
          setMovieId(res.data.data.public_id);
          setLikes(res.data.data.thumbs_up);
          setViews(res.data.data.popular);
        })
        .catch(err => console.log("Sorry, can't fetch movie detail!", err));
    }
    fetchDetail();
	}, []);
	
	// Helper Methods
	const connect = e => {
		setShowFriends(false);
		setShowChat(true);
	};

	const disconnect = e => {
		setShowFriends(true);
		setShowChat(false);
	};

  const handleSubmit = e => {
    e.preventDefault();
    alert("Sent!");
  };

  const startVideoCall = e => {

  };

  const SimilarMovies = () => {
    // fetch data from api using u_id
    // console.log("Props Id: " + props.id);
    const [movies, setMovies] = useState([]);
    const [movie_length, setMoviesLength] = useState(0);
    useEffect(() => {
      const GetSimilarMovies = async () => {
        try {
          const res = await axios.get("https://movie-stream-api.herokuapp.com/api/similar/movie/"+ movie_id);
          console.log("Similar Movies: ", res);
          // set the value of similarMovies variable to the response
          setMovies(res.data.data);
          setMoviesLength(res.data.data.length);
        } catch (err) {
          console.log(err);
        }
      };
      GetSimilarMovies();
    }, []);
  
    return <div className="recommended">
            {/* <p className="title">{ movies.length != 0 ? "You might also like" : null }</p> */}
            <div className="show">
              {/* {movies.map((i, idx) => <MovieCard title={i.title} liked={i.liked} key={idx} viewed={i.viewed} />)} */}
            </div>
          </div>
	};
	
	// Friends component
	const Friend = ({ pic, name, address }) => {
		const imgStyle = {};
		return (
			<div className="friend">
				<div class="imgFrame">
					<img src={pic} alt="." style={imgStyle} />
				</div>
				<div className="detail">
					<h3>{name}</h3>
					<p>
						<a href="#">{address}</a>
						<button className="connectBtn" onClick={connect}>Connect</button>
					</p>
				</div>
			</div>
		);
	};

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
                poster={`https://res.cloudinary.com/dymhlpm8a/video/upload/${movie_name}.jpg`}
                autoPlay={true}
                controls={true}
                className="theShow"
              >
                {/* <source src={`https://res.cloudinary.com/dymhlpm8a/video/upload/${movie_name}`} type="video/webm"/>
                <source src={`https://res.cloudinary.com/dymhlpm8a/video/upload/${movie_name}`} type="video/mp4"/>
                <source src={`https://res.cloudinary.com/dymhlpm8a/video/upload/${movie_name}`} type="video/ogg"/> */}
              </video>
            </div>
            <div className="actions">
              <p className="title">{movie_name}</p>
              <div className="btns">
                <div>
                  <FaHeart className="icons" /> <br />
                  <span>{likes}</span>
                </div>
                <div>
                  <FaEye className="icons" /> <br />
                  <span>{views}</span>
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
          <div class="room">
						{
							showFriends && (
								<>
									<header>
										<h3 class="center">Friends</h3>
									</header>
									<div class="friends">
										<Friend 
											pic={Joker}
											name="Jane"
											address="@jane1553"
											status={true}
											title="The Avengers"
										/>
										<Friend 
											pic={Joker}
											name="Jane"
											address="@jane1553"
											status={true}
											title="The Avengers"
										/>
										<Friend 
											pic={Joker}
											name="Jane"
											address="@jane1553"
											status={true}
											title="The Avengers"
										/>
										<Friend 
											pic={Joker}
											name="Jane"
											address="@jane1553"
											status={true}
											title="The Avengers"
										/>
										<Friend 
											pic={Joker}
											name="Jane"
											address="@jane1553"
											status={true}
											title="The Avengers"
										/>
									</div>
								</>
							)
						}
						{
							showChat && (
								<div className="chat">
									<header>
										<div>
                			<FaArrowLeft size={20} color="white" onClick={disconnect} />
											<span>Jane</span>
										</div>
										<img src={logo} alt="." onClick={startVideoCall} />
									</header>
									<div className="chatBoard">
										{/* The chat */}
									</div>
                  <form onSubmit={handleSubmit}>
                    <input type="text" className="inp" placeholder="Message" />
                    <button type="submit">Send</button>
                  </form>
								</div>
							)
						}
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
        <SimilarMovies />
      </div>
      <SubcribeLayout />
      <Footer />
    </div>
  );
};

export default Watch;
