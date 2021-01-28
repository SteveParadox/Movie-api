import React, { useEffect, useContext } from "react";
import { NavLink, Link } from "react-router-dom";
import "../styles/AppNavBar.css";
import logo from "../video-camera.svg";
import { MovieContext } from "../MovieContext";
import { FaSearch, FaAngleDown, FaBell } from "react-icons/fa";
import Friend from "./Friend";
import axios from "axios";
import urls from "../apiEndPoints";

// Bring in img for testing purpose
import Joker from "../joker_movie.jpg";
import User from "../user.jpg";


const UserAvatar = (props) => {
  return (
    <div className="user-avatar">
      <img src={User} alt="User Avatar" />
      {/* <span className="number-of-users"> {props.numberOfUsers} </span> */}
      <FaAngleDown size={18} color={"grey"} />
    </div>
  );
};

const AppNavBar = () => {
  const [appState, setAppState] = useContext(MovieContext);

  useEffect(() => {
    function fetchData() {
      axios(urls.all)
        .then(res => {
          setAppState(n => {
            return {
              ...n,
              logged_in: res.data["logged in"],
              user_name: res.data["name"] ? res.data["name"] : ""
            }
          })
        })
        .catch(() => console.log("Something went wrong!"));
    }
    fetchData();
  })

  // Helper functions
  function openFindFriends() {
    setAppState(prevState => ({...prevState, friendsDisplay: true }));
  }
  
  function closeFindFriends() {
    setAppState(prevState => ({...prevState, friendsDisplay: false }));
  }

  const friendDisplay1 = {
    "transform": "translateX(-290px)",
  };

  const friendDisplay2 = {
    "transform": "translateX(0px)",
  };

  const logoVisibility1 = {
    "visibility": "hidden",
  };

  const logoVisibility2 = {
    "visibility": "visible",
  };

  return (
    <nav className="navbar">
      <div className="find-friends" style={appState.friendsDisplay ? friendDisplay2 : friendDisplay1 }>
        <div className="find-input">
          <span>
            <FaSearch size={20} color="grey"/>
          </span>
          <input type="text" name="find_friends" id="find_friends" placeholder="find friends" />
          <span className="closeFindFriends" onClick={closeFindFriends}>&times;</span>
        </div>

        <div className="friend-results">
          <Friend avatar={Joker} name="Nonso" status={true} title="The Avengers" />
          <Friend avatar={Joker} name="Jane" status={true} title="The Avengers" />
          <Friend avatar={Joker} name="Anita" status={false} into="Actions, thriller, Horror" />
        </div>
      </div>
      <div className="top-bar">
        {/* The logo */}
        <div className="logo" style={ appState.friendsDisplay ? logoVisibility1 : logoVisibility2 }>
          <img src={logo} id="cam-logo" width={25} height={25} alt="logo" onClick={openFindFriends} />
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
              <FaBell size={27} color="white"/>
              <span id="notification-number">2</span>
            </button>
          </Link>
          <Link to="/user">
            <UserAvatar numberOfUsers={2} />
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default AppNavBar;
