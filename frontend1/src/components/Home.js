import React, { useContext, useEffect } from "react";
import { Redirect } from "react-router-dom";
// import axios from "axios";
// import url from "../apiEndPoints";

// The components
import AppNavBar from "./AppNavBar";
import Banner from "./TestBanner";
// import Watching from "./Watching";
import Recommendations from "./Recommendations";
import Movies from "./Movies";
import SubscribeLayout from "./SubscribeLayout";
import Footer from "./Footer";
import { MovieContext } from "../MovieContext";

function Home() {
  const [appState, setAppState] = useContext(MovieContext);

  useEffect(() => {
    // const token = localStorage.getItem("token");
    // console.log(token);
    if(!appState.logged_in) {
      if(localStorage.getItem("token")) {
        setAppState(n => {
          return {
            ...n,
            logged_in: true
          }
        });
      }
    }
    // eslint-disable-next-line
  }, []);

  return (
    <div>
      {!appState.logged_in ? <Redirect to="/signin" /> : null}
      <AppNavBar />
      <Banner />
      {/* <Watching /> */}
      <Recommendations />
      <Movies />
      <SubscribeLayout />
      <Footer />
    </div>
  );
}

export default Home;