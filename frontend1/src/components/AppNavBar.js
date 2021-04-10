import React, { useContext, useState, createRef } from "react";
import { NavLink, Link } from "react-router-dom";
import "../styles/AppNavBar.css";
import logo from "../video-camera.svg";
import { MovieContext } from "../MovieContext";
import { FaSearch, FaAngleDown, FaBell, FaArrowLeft, FaAngleRight, FaMixcloud } from "react-icons/fa";
import { BsFillCameraVideoFill } from "react-icons/bs";
import { TiArrowSortedDown } from "react-icons/ti";
import { MdMovie } from "react-icons/md";
import { AiFillDatabase } from "react-icons/ai";
import Friend from "./Friend";
// import axios from "axios";
// import urls from "../apiEndPoints";

// Bring in img for testing purpose
import Joker from "../joker_movie.jpg";
import User from "../user.jpg";
import axios from "axios";

const UserAvatar = (props) => {
  return (
    <div className="user-avatar">
      <img src={User} alt="User Avatar" />
      {/* <span className="number-of-users"> {props.numberOfUsers} </span> */}
      <FaAngleDown size={18} color={"grey"} />
    </div>
  );
};

const AppNavBar = (props) => {
  const [appState, setAppState] = useContext(MovieContext);
  const [navOpen, setNavOpen] = useState(false);
  const [turn, setTurn] = useState(false);
  // const [logged_in, setLogged] = useState(false);
  const burger = createRef();

  const logout = () => {
    axios.post("movie-stream-api.herokuapp.com", {
      "token": localStorage.getItem("token")
    })
    .then(res => {
      // Update storage
      localStorage.removeItem("token");
      props.history.push("/signin");
    })
    .catch(err => {
      // Update UI reporting failure to logout
    })
  }

  // Check and store logged in
  // useEffect(() => {
  //   function fetchData() {
  //     axios.get(urls.all)
  //       .then(res => {
  //         console.log(res);
  //         setLogged(res.data["logged in"]);
  //         console.log(res.data["logged in"]);
  //         setAppState(n => {
  //           return {
  //             ...n,
  //             logged_in: res.data["logged in"],
  //             user_name: res.data["name"] ? res.data["name"] : ""
  //           }
  //         })
  //       })
  //       .catch(() => console.log("Something went wrong!"));
  //   }
  //   fetchData();
  // }, []);

  // Helper functions
  function openFindFriends() {
    setAppState((prevState) => ({ ...prevState, friendsDisplay: true }));
  }

  function closeFindFriends() {
    setAppState((prevState) => ({ ...prevState, friendsDisplay: false }));
  }

  const friendDisplay1 = {
    transform: "translateX(-290px)",
  };

  const friendDisplay2 = {
    transform: "translateX(0px)",
  };

  const logoVisibility1 = {
    visibility: "hidden",
  };

  const logoVisibility2 = {
    visibility: "visible",
  };

  const closeMobileNav = (e) => {
    e.stopPropagation();
    setNavOpen(false);
  }

  const openMobileNav = (e) => {
    e.stopPropagation();
    setNavOpen(true);
  }
  
  return (
    <nav className="navbar">
      {/* { !logged_in ? <Redirect to="/signin" /> : null} */}
      <div
        className="find-friends"
        style={appState.friendsDisplay ? friendDisplay2 : friendDisplay1}
      >
        <div className="find-input">
          <span>
            <FaSearch size={20} color="grey" />
          </span>
          <input
            type="text"
            name="find_friends"
            id="find_friends"
            placeholder="find friends"
          />
          <span className="closeFindFriends" onClick={closeFindFriends}>
            &times;
          </span>
        </div>

        <div className="friend-results">
          <Friend
            avatar={Joker}
            name="Nonso"
            status={true}
            title="The Avengers"
          />
          <Friend
            avatar={Joker}
            name="Jane"
            status={true}
            title="The Avengers"
          />
          <Friend
            avatar={Joker}
            name="Anita"
            status={false}
            into="Actions, thriller, Horror"
          />
        </div>
      </div>
      <div className="top-bar">
        {/* The logo */}
        <div
          className="logo"
          style={appState.friendsDisplay ? logoVisibility1 : logoVisibility2}
        >
          <img
            src={logo}
            id="cam-logo"
            width={25}
            height={25}
            alt="logo"
            onClick={openFindFriends}
          />
          {/* <BsFillCameraVideoFill size={22} color="white" onClick={openFindFriends} id="cam-logo" /> */}
          <h3>Filba</h3>
        </div>

        {/* The links */}
        <ul className="nav-links">
          <NavLink exact activeClassName="active" to="/">
            <li>Home</li>
          </NavLink>
          <NavLink activeClassName="active" to="/movies">
            <li>Movies</li>
          </NavLink>
          {/* <NavLink activeClassName="active" to="/series">
            <li>Series</li>
          </NavLink>
          <NavLink activeClassName="active" to="/live">
            <li>Live</li>
          </NavLink> */}
          <NavLink activeClassName="active" to="/list">
            <li>My List</li>
          </NavLink>
        </ul>

        {/* The search, notification and user */}
        <div className="snu">
          <Link to="/search">
            <button className="search">
              <FaSearch size={27} color="white" />
            </button>
          </Link>
          <Link to="/notification">
            <button className="notification">
              <FaBell size={27} color="white" />
              <span id="notification-number">2</span>
            </button>
          </Link>
          <Link to="/user">
            <UserAvatar numberOfUsers={2} />
          </Link>
        </div>
      </div>
      <div className="mobile" onClick={openMobileNav}>
          <div className="burger">
            <div className="line1"></div>
            <div className="line1"></div>
            <div className="line1"></div>
          </div>
        <div className="actions" ref={burger} style={{"transform": navOpen === true ? "translateY(0)" : "translateY(-900px)"}}>
          <div className="top">
            <FaArrowLeft className="icon arrow-left" onClick={closeMobileNav}/>
            <h3 className="title">Activity</h3>
          </div>
          <div className="nav-body">
            <Link to="/user">
              <div className="profile">
                <img src={Joker} alt="." className="dp"/>
                <div className="details">
                  <h3>@Nonso</h3>
                  <p>Visit Profile</p>
                </div>
                <FaAngleRight className="nav-arrows"/>
              </div>
            </Link>

            <div className="Movies" style={{height: !turn ? "60px" : "220px"}}>
              <div className="details">
                <h3>Movies</h3>
                <p>Your movie categories</p>
              </div>
              <TiArrowSortedDown onClick={() => setTurn(n => !n)} className="nav-arrows movie-arrow" style={{ "transform": turn ? "scaleY(-1)" : "scaleY(1)" }}/>
              <div className="other" style={{display: !turn ? "none" : "block"}}>
                <Link to="/movies"><p className="active-mobile"><MdMovie className="icons" />Movies</p></Link>
                <Link><p><AiFillDatabase className="icons" /> Series</p></Link>
                <Link><p><FaMixcloud className="icons" /> Live</p></Link>
              </div>
            </div>

            <Link>
              <div className="My List">
                <div className="details">
                  <h3>My List</h3>
                  <p>View your saved movies</p>
                </div>
                <FaAngleRight className="nav-arrows"/>
              </div>
            </Link>

            <Link>
              <div className="Settings">
                <div className="details">
                  <h3>Settings</h3>
                  <p>View your privacy policy, etc</p>
                </div>
                <FaAngleRight className="nav-arrows"/>
              </div>
            </Link>

            <Link>
              <div className="Friend Request">
                <div className="details">
                  <h3>Friend Request</h3>
                  <p>Respond to friend requests</p>
                </div>
                <FaAngleRight className="nav-arrows"/>
              </div>
            </Link>

            <Link>
              <div className="Logout" onClick={logout}>
                <div className="details">
                  <h3>Logout</h3>
                  <p>Sign out</p>
                </div>
              <FaAngleRight className="nav-arrows"/>
              </div>
            </Link>
          </div>
        </div>
          
        <div className="logo">
          <BsFillCameraVideoFill className="icon" />
          <span>Filba</span>
        </div>
        <div className="search">
          <Link to="/search">
            <FaSearch className="icon" onClick={openFindFriends} />
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default AppNavBar;

