import React, { Component } from "react";
import "./App.css";

import { MovieProvider } from "./MovieContext";

// The components
import AppNavBar from "./components/AppNavBar";
import Banner from "./components/Banner";
import Watching from "./components/Watching";
import Recommendations from "./components/Recommendations";
import Movies from "./components/Movies";
import SubscribeLayout from "./components/SubscribeLayout";
import Footer from "./components/Footer";

class App extends Component {
  render() {
    return (
      <MovieProvider>
        <div className="App">
          {/* <AppNavBar /> */}
          {/* <Banner /> */}

          {/* <Watching />
          <Recommendations />
          <Movies /> */}

          {/* Finished components */}
          {/* <SubscribeLayout /> */}
          {/* <Footer /> */}
        </div>
      </MovieProvider>
    );
  }
}

export default App;
