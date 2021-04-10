import React, { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { MovieContext } from "../MovieContext";
import MovieCard from "./MovieCard";
import "../styles/MovieCard.css";
import { FaPlus, FaStar, FaFire, FaPlayCircle } from "react-icons/fa";
import { BiTrendingUp } from "react-icons/bi";
// import { GiAerialSignal } from "react-icons/gi";
import { GoPrimitiveDot } from "react-icons/go";
import { MdMovie } from "react-icons/md";
import "../styles/Movies.css";
import axios from "axios";
import urls from "../apiEndPoints";


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
  const [MoviesState, setMovieState] = useState([]);
  const [set, setSet] = useState(1);
  // movies state should hold data to be mapped(displayed) to the screen
  // @todo -> using the useEffect hook, update the movies state based
  // on the genre state, by making calls to the server
  const [genres, updateGenres] = useState({
    action: true,
    comedy: false,
    horror: true,
    documentary: false,
    mystery: true,
    animation: true,
    "sci-fi": true,
    romance: false,
    erotic: false,
    fantasy: false,
    drama: true,
    thriller: true,
    children: false,
    family: true,
    crime: true,
  });

  // Fetch movies for display
  useEffect(() => {
    function fetchMovies() {
      axios.get(urls.popular)
        .then(res => {
          // console.log(res.data);
          setMovieState(res.data.data);
        })
        .catch(err => console.log("Sorry fetch movies failed", err));
    }
    fetchMovies();
  },[setMovieState]);

  window.addEventListener("click", (e) => {
    window.test = e.target;
    if(e.target.nodeName === "svg") return;
    if(!e.target.className.includes) return;
    if(!e.target.className.includes("specX")) {
      updateState((n) => {
        return {
          ...n,
          detailsDisplay: false,
        };
      });
    }
  });

  // get the ui_id from the state and do a fetch call to get the movie data
  const MovieDetails = () => {
    const closeDetails = (e) => {
      // console.log(e);

      updateState((n) => {
        return {
          ...n,
          detailsDisplay: false,
        };
      });
    };
    
    const place = {
      top: state.details.top,
      display: state.detailsDisplay ? "flex" : "none",
    };
    const svgCenter = {
      left: state.details.left,
    };
    const bg = {
      background: `url("https://res.cloudinary.com/dymhlpm8a/image/upload/${state.details.title}.jpg")`,
      // background: `url(${Joker})`,
      backgroundPosition: "center",
      backgroundRepeat: "no-repeat",
      backgroundSize: "100% 150%",
      height: "100%",
      borderTopRadius: "4px",
      borderBottomRadius: "4px",
    };
    return (
        <div className="details specX" style={place}>
          <svg
            id="arrow"
            baseProfile="full"
            zmlns="http://www.w3.org/2000/svg"
            style={svgCenter}
            className="specX"
          >
            <polygon width="45" height="45" points="22.5, 0 45,45 0,45" />
          </svg>
          <div className="vidShow specX" style={bg}>
            {/* <img src={`https://res.cloudinary.com/du05mneox/image/upload/${state.details.title}.jpg`} alt="."/> */}
            <Link to={`/watch/${state.details.u_id}`}>
              <FaPlayCircle className="icon specX" />
            </Link>
          </div>
          <div className="all-details specX">
            <div className="title specX">
              <h3>{state.details.title}</h3>
              <span><FaStar color="yellow" /> {state.details.rating}/10</span>
            </div>
            <div className="year-genre specX">
              <span className="year">{state.details.year}</span>
              <GoPrimitiveDot className="dot" />
              <span className="genre specX">{state.details.genre}</span>
            </div>
            <p className="desc specX">{state.details.desc.slice(0, 300)}</p>
            <p className="director specX"><span>Director:</span> {state.details.director}</p>
            <Link to="/watch/dkjdk" className="relMovies specX">Related Movies</Link>
            <span className="closeBtn specX" onClick={closeDetails}>
              {/* <FaWindowClose /> */}
              &times;
            </span>
          </div>
        </div>
    );
  };

  const showDetails = (e) => {
    e.stopPropagation();
    let elem = e.target;
    let movie_id = elem.attributes["data-movie-id"].value;
    let movie_desc = elem.attributes["data-movie-desc"].value;
    let movie_name = elem.attributes["data-movie-title"].value;
    let movie_genre = elem.attributes["data-movie-genre"].value;
    let movie_review = elem.attributes["data-movie-review"].value;
    let movie_director = elem.attributes["data-movie-director"].value;
    let movie_year = elem.attributes["data-movie-year"].value;

    // console.log(elem);
    updateState((n) => {
      return {
        ...n,
        details: {
          top: elem.offsetTop,
          left: elem.offsetLeft,
          u_id: movie_id,
          title: movie_name,
          desc: movie_desc,
          genre: movie_genre,
          rating: movie_review,
          director: movie_director,
          year: movie_year
        },
        detailsDisplay: true,
      };
    });
    // console.log(state);
      // the movie id
      // use the movie id to fetch the movie data from the api
  };

  const addGenre = (e) => {
    // get the name of genre from button first
    const genreName = e.target.attributes["data-genre-name"].value;
    updateGenres((n) => {
      return {
        ...n,
        [genreName]: !n[genreName],
      };
    });
  };

  const showMovies = () => {
    setSet(1);
    axios.post("https://movie-stream-api.herokuapp.com/api/choice", {
      "token": localStorage.getItem("token"),
    })
      .then(res => {
        setMovieState(res.data.data);
      })
      .catch(err => console.log("Failed fetcing movies"));
  };

  const showPopular = () => {
    setSet(2);
    axios.get("https://movie-stream-api.herokuapp.com/api/popular")
      .then(res => {
        setMovieState(res.data.data);
      })
      .catch(err => console.log("Failed fetcing movies"));
  };

  const showTrending = () => {
    setSet(3);
    axios.get("https://movie-stream-api.herokuapp.com/api/trending")
      .then(res => {
        setMovieState(res.data.data);
      })
      .catch(err => console.log("Failed fetcing movies"));
  };

  const showoPremieres = () => {
    setSet(4);
    axios.post("https://movie-stream-api.herokuapp.com/api/", {
      "token": localStorage.getItem("token")
    })
      .then(res => {
        setMovieState(res.data.data);
      })
      .catch(err => console.log("Failed fetcing movies"));
  };

  return (
    <div className="movies">
      <div className="top">
        <h3 className={set === 1 ? "active" : ""} onClick={showMovies}>
          {" "}
          <MdMovie /> Movies
        </h3>
        <h3 className={set === 2 ? "active" : ""} onClick={showPopular}>
          {" "}
          {/* <FaFilm /> Series */}
          <FaFire /> Popular
        </h3>
        <h3 className={set === 3 ? "active" : ""} onClick={showTrending}>
          {" "}
          {/* <GiAerialSignal /> Live Streams */}
          <BiTrendingUp /> Trending
        </h3>
        <h3 className={set === 4 ? "active" : ""} onClick={showoPremieres}>
          {" "}
          <FaStar /> Premieres
        </h3>
      </div>

      <div className="genres">
        {/* <button onClick={addGenre} data-genre-name="trending"><BiTrendingUp /> Trending</button> */}
        {/* <button onClick={addGenre} data-genre-name="popular"><FaFire /> Popular</button> */}
        {/* <button onClick={addGenre} data-genre-name="premieres"><FaStar /> Premieres</button> */}
        {/* <button onClick={addGenre} data-genre-name="adventure">Adventure</button> */}
        <button
          onClick={addGenre}
          data-genre-name="drama"
          style={{ background: genres["drama"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Drama
        </button>
        <button
          onClick={addGenre}
          data-genre-name="horror"
          style={{ background: genres["horror"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Horror
        </button>
        <button
          onClick={addGenre}
          data-genre-name="comedy"
          style={{ background: genres["comedy"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Comedy
        </button>
        <button
          onClick={addGenre}
          data-genre-name="action"
          style={{ background: genres["action"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Action
        </button>
        <button
          onClick={addGenre}
          data-genre-name="documentary"
          style={{ background: genres["documentary"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          documentary
        </button>
        <button
          onClick={addGenre}
          data-genre-name="sci-fi"
          style={{ background: genres["sci-fi"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Sci-fi
        </button>
        <button
          onClick={addGenre}
          data-genre-name="romance"
          style={{ background: genres["romance"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Romance
        </button>
        <button
          onClick={addGenre}
          data-genre-name="erotic"
          style={{ background: genres["erotic"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Erotic
        </button>
        <button
          onClick={addGenre}
          data-genre-name="thriller"
          style={{ background: genres["thriller"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Thriller
        </button>
        <button
          onClick={addGenre}
          data-genre-name="family"
          style={{ background: genres["family"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          family
        </button>
        <button
          onClick={addGenre}
          data-genre-name="children"
          style={{ background: genres["children"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Children
        </button>
        <button
          onClick={addGenre}
          data-genre-name="mystery"
          style={{ background: genres["mystery"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Mystery
        </button>
        <button
          onClick={addGenre}
          data-genre-name="fantasy"
          style={{ background: genres["fantasy"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Fantasy
        </button>
        <button
          onClick={addGenre}
          data-genre-name="animation"
          style={{ background: genres["animation"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Animation
        </button>
        <button
          onClick={addGenre}
          data-genre-name="crime"
          style={{ background: genres["crime"] ? "var(--apps-red)" : "#2b2a30" }}
        >
          Crime
        </button>
        {/* <button onClick={addGenre} data-genre-name="history">Historical</button> */}
        {/* <button onClick={addGenre} data-genre-name="magical">Magical</button> */}
      </div>

      <div className="sort">
        <div>
          Sort by:{" "}
          <select name="sortAlphabet" id="sortAlphabet">
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
        {/* <div 
          onClick={showDetails} 
          data-movie-id={"5"}
          data-movie-desc={"blah ".repeat(40)}
          data-movie-title={"The Nun"}
          data-movie-genre={"Horror"}
          data-movie-review={6.5}
          data-movie-director={"uche Jombo"}
          data-movie-year={"2018-12-4 23"}
        >
          <MovieCard title="Stuff" like={true} viewed={true} />
        </div> */}
        {
          MoviesState.map((i, idx) => (
            <div 
              key={idx} 
              data-movie-id={i.id} 
              data-movie-desc={i.description}
              data-movie-title={i.name}
              data-movie-genre={i.genre}
              data-movie-review={i.review}
              data-movie-director={i.creator}
              data-movie-year={i.created_on}
              onClick={showDetails}
            >
              <MovieCard title={i.name} like={i.thumbs_up} viewed={i.popular} />
            </div>
          ))
        }
      </div>
      <PlusMovies />
    </div>
  );
};

export default Movies;
