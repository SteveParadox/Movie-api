import React, { useContext, useState } from "react";
import { MovieContext } from "../MovieContext";
import "../styles/MoviesSection.css";
import MovieCard from "./MovieCard";
import "../styles/MovieCard.css";
import { FaPlus, FaStar, FaFilm, FaFire, FaPlayCircle, FaSearch } from "react-icons/fa";
import { BiTrendingUp } from "react-icons/bi";
import { GiAerialSignal } from "react-icons/gi";
import { MdMovie } from "react-icons/md";
import "../styles/Movies.css";
import Joker from "../joker_movie.jpg";

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


const Movies = () => {
  const [state, updateState] = useContext(MovieContext);
  // movies state should hold data to be mapped(displayed) to the screen
  // @todo -> using the useEffect hook, update the movies state based
  // on the genre state, by making calls to the server
  const [genres, updateGenres] = useState({
    "action": true,
    "comedy": false,
    "horror": true,
    "documentary": false,
    "mystery": true,
    "animation": true,
    "sci-fi": true,
    "romance": false,
    "erotic": false,
    "fantasy": false,
    "drama": true,
    "thriller": true,
    "children": false,
    "family": true,
    "crime": true
  });
  // get the ui_id from the state and do a fetch call to get the movie data
  const MovieDetails = () => {
    const closeDetails = () => {
      console.log("Blurred");
      debugger;
      updateState(n => {
        return {
        ...n,
        detailsDisplay: false
        }
      });
    };
    const place = {
      "top": state.details.top,
      "display": state.detailsDisplay ? "block" : "none",
    }
    const svgCenter = {
      "left": state.details.left
    }
    const bg = {
      "background": `url(${Joker})`,
      "backgroundPosition": "center",
      "backgroundRepeat": "no-repeat",
      "backgroundSize": "cover",
      "height": "100%",
      "borderTopRadius": "4px",
      "borderBottomRadius": "4px",
    }
    return (
      <div className="details" style={place} onBlur={closeDetails}>
        <svg
         id="arrow"
         baseProfile="full"
         zmlns="http://www.w3.org/2000/svg"
         style={svgCenter}
        >
          <polygon width="45" height="45" points="22.5,0 45,45 0,45"/>
         </svg>
         <div className="thumb" style={bg}>
           {/* display play button here at the center */}
           <FaPlayCircle size={60} color="lightgrey" />
         </div>
        {/* <p>{state.details.ui_id}</p> */}
        <div className="all-details">
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet quam enim, dolorum repudiandae error id eum autem? Delectus eum earum ipsum itaque nam. Assumenda ipsum adipisci itaque nihil porro nam, quas reprehenderit suscipit deleniti molestiae mollitia architecto aliquid libero odio provident voluptatibus ipsa fugit excepturi!</p>
          <p> {state.details.ui_id} </p>
        </div>
      </div>
    );
  }
  
  const showDetails = (e) => {
    if(e.target.nodeName === "IMG") {
       let elem = e.target.parentNode.parentNode.parentNode;
       let movie_id = elem.attributes["data-movie-id"].value;
       console.log(elem);
       console.log("Movie ID:", movie_id);
       updateState(n => {
         return {
           ...n,
           details: {
             top: elem.offsetTop,
             left: elem.offsetLeft,
             ui_id: movie_id
           },
           detailsDisplay: true
         }
       });
       console.log(state);
       // the movie id
       // use the movie id to fetch the movie data from the api
    }
  }

  const addGenre = e => {
    // get the name of genre from button first
    const genreName = e.target.attributes["data-genre-name"].value;
    updateGenres(n => {
      return {
        ...n,
        [genreName]: !n[genreName]
      }
    })
  }
  
  return (
    <div className="movies">

      <div className="top">
        <h3 className="active"> <FaSearch /> Search</h3>
        <h3> <BiTrendingUp /> Trending</h3>
        <h3> <FaFire /> Popular</h3>
        <h3> <FaStar /> Mood</h3>
      </div>

      <div className="searchInput">
        <input type="text"/>
        <FaSearch color="grey" />
      </div>

      <div className="genres">
        {/* <button onClick={addGenre} data-genre-name="trending"><BiTrendingUp /> Trending</button> */}
        {/* <button onClick={addGenre} data-genre-name="popular"><FaFire /> Popular</button> */}
        {/* <button onClick={addGenre} data-genre-name="premieres"><FaStar /> Premieres</button> */}
        {/* <button onClick={addGenre} data-genre-name="adventure">Adventure</button> */}
        <button onClick={addGenre} data-genre-name="drama" style={{"background": genres["drama"] ? "red": "#2b2a30"}}>Drama</button>
        <button onClick={addGenre} data-genre-name="horror" style={{"background": genres["horror"] ? "red": "#2b2a30"}}>Horror</button>
        <button onClick={addGenre} data-genre-name="comedy" style={{"background": genres["comedy"] ? "red": "#2b2a30"}}>Comedy</button>
        <button onClick={addGenre} data-genre-name="action" style={{"background": genres["action"] ? "red": "#2b2a30"}}>Action</button>
        <button onClick={addGenre} data-genre-name="documentary" style={{"background": genres["documentary"] ? "red": "#2b2a30"}}>documentary</button>
        <button onClick={addGenre} data-genre-name="sci-fi" style={{"background": genres["sci-fi"] ? "red": "#2b2a30"}}>Sci-fi</button>
        <button onClick={addGenre} data-genre-name="romance" style={{"background": genres["romance"] ? "red": "#2b2a30"}}>Romance</button>
        <button onClick={addGenre} data-genre-name="erotic" style={{"background": genres["erotic"] ? "red": "#2b2a30"}}>Erotic</button>
        <button onClick={addGenre} data-genre-name="thriller" style={{"background": genres["thriller"] ? "red": "#2b2a30"}}>Thriller</button>
        <button onClick={addGenre} data-genre-name="family" style={{"background": genres["family"] ? "red": "#2b2a30"}}>family</button>
        <button onClick={addGenre} data-genre-name="children" style={{"background": genres["children"] ? "red": "#2b2a30"}}>Children</button>
        <button onClick={addGenre} data-genre-name="mystery" style={{"background": genres["mystery"] ? "red": "#2b2a30"}}>Mystery</button>
        <button onClick={addGenre} data-genre-name="fantasy" style={{"background": genres["fantasy"] ? "red": "#2b2a30"}}>Fantasy</button>
        <button onClick={addGenre} data-genre-name="animation" style={{"background": genres["animation"] ? "red": "#2b2a30"}}>Animation</button>
        <button onClick={addGenre} data-genre-name="crime" style={{"background": genres["crime"] ? "red": "#2b2a30"}}>Crime</button>
        {/* <button onClick={addGenre} data-genre-name="history">Historical</button> */}
        {/* <button onClick={addGenre} data-genre-name="magical">Magical</button> */}
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
      <MovieDetails />  
      <div className="displayMovies">
        <div onClick={showDetails} data-movie-id={"1"}>
          <MovieCard title="Stuff" like={true} viewed={true}/>
        </div>
        <div onClick={showDetails} data-movie-id={"2"}>
          <MovieCard title="Stuff" like={true} viewed={true} />
        </div>
        <div onClick={showDetails} data-movie-id={"3"}>
          <MovieCard title="Stuff" like={true} viewed={true} />
        </div>
        <div onClick={showDetails} data-movie-id={"4"}>
          <MovieCard title="Stuff" like={true} viewed={true} />
        </div>
        <div onClick={showDetails} data-movie-id={"5"}>
          <MovieCard title="Stuff" like={true} viewed={true} />
        </div>
      </div>
      <PlusMovies />
    </div>
  );
}

export default Movies;