import React, { useState, useEffect, useContext } from 'react';
import { MovieContext } from "../MovieContext";
import { Redirect } from "react-router-dom";
import { FaEdit, FaPencilAlt, FaArrowLeft } from "react-icons/fa";
import AppNavBar from "./AppNavBar";
import Footer from "./Footer";
import "../styles/User.css";
import dp from "../user.jpg";
import axios from "axios";
import urls from "../apiEndPoints";

function User() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [appState, setAppState] = useContext(MovieContext);
  // First use the useEffect hook to check if user is logged in
  // on clicking logout simply set loggedIn state to false.
  
  // if(!appState.logged_in) {
  //   return (
  //     <Redirect to="/signin" />
  //   );
  // }

  // function change(reqData) {
  //   Object.keys(reqData).map(function(key) {
  //     return encodeURIComponent(key) + '=' + encodeURIComponent(reqData[key])
  //   }).join('&')
  // }

  return (
    <div className="user-page">
      {!appState.logged_in ? <Redirect to="/signin" /> : 
        <>
          <AppNavBar />
          {/* Special Nav */}
          <div className="special-nav">
            <FaArrowLeft className="icon" />
            <p>Profile</p>
          </div>
          <div className="main">
            <div className="dp">
              <div>
                <img src={dp} alt="."/>
                <button className="editPic bordered" title="Change Picture"><FaPencilAlt className="icons"/></button>
              </div>
            </div>
            <div className="details">
              <div className="name">
                <p className="">Name Surname</p>
                <span className="edit"><FaPencilAlt className="icons"/></span>
              </div>
              <div className="friends">
                <button className="noborder">Friends</button>
                <button className="noborder">Close Friends</button>
              </div>
              <div className="bio">
                <p>Bio</p>
                <p className="bio-desc">Lorem ipsum dolor sit amet consectetur adipisicing elit. Nisi dolore consequuntur adipisci sapiente placeat esse doloribus eos! Modi eos blanditiis totam porro illo omnis expedita animi quia veritatis aspernatur! Saepe, aspernatur! Autem?</p>
              </div>
              <div className="collections">
                <div className="center">
                  <p>My Collections</p>
                  <span className="edit"><FaPencilAlt className="icon" /></span>
                </div>
                <div className="slide">
                  Slider - Coming Soon
                </div>
              </div>
            </div>
            <div className="interest">
              <div className="all">
                <div className="center">
                  <p>My interest</p>
                  <span className="edit">
                    <FaPencilAlt />
                  </span>
                </div>
                <div className="content">
                  <div className="item">
                    <h3>Genre</h3>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                  </div>

                  <div className="item">
                    <h3>Actor/Actress</h3>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                  </div>

                  <div className="item">
                    <h3>Director</h3>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                  </div>

                  <div className="item">
                    <h3>Favorite</h3>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                    <p>Lorem ipsum dolor sit amet.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <Footer />
        </>
      }
    </div>
  );
}

export default User;