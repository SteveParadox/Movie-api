import React, { useEffect, useContext, useState } from "react";
import { NavLink, Link, Redirect } from "react-router-dom";
import "../styles/AppNavBar.css";
import logo from "../video-camera.svg";
import { MovieContext } from "../MovieContext";
import { FaSearch, FaAngleDown, FaBell, FaArrowLeft } from "react-icons/fa";
import { BsFillCameraVideoFill } from "react-icons/bs";
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
  const [navOpen, setNavOpen] = useState(false);
  const [logged_in, setLogged] = useState(false);

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

  const closeMobileNav = () => {
    try {
      setNavOpen(false);
    } catch(err) {
      console.log(err);
    }
    console.log(navOpen);
    console.log(setNavOpen.toString());
  }

  const openMobileNav = () => {
    try {
      setNavOpen(true);
    } catch(err) {
      console.log(err);
    }
    console.log(navOpen);
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
        <div className="actions" style={{"display": navOpen ? "block" : "none"}}>
          <div className="top">
            <FaArrowLeft className="icon" onClick={closeMobileNav}/>
            <h3 className="title">Activity</h3>
          </div>
          <div className="nav-body">
            <div className="profile">
              Profile
            </div>
            <div className="Movies">
              Movies
            </div>
            <div className="My List">
              My List
            </div>
            <div className="Settings">
              Settings
            </div>
            <div className="Friend Request">
              Friend Request
            </div>
            <div className="Messages">
              Messages
            </div>
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
