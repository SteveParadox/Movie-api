import React from 'react';

// Import components
import AppNavBar from "./AppNavBar";
import Banner from "./TestBanner";
import Watching from "./Watching";
import Recommendations from "./Recommendations";
import MoviesSection from "./MoviesSection";
import SubscribeLayout from "./SubscribeLayout";
import Footer from "./Footer";

const MoviesRoute = (props) => {
  return ( 
    <div className="mvpage">
      <AppNavBar />
      <Banner />
      <Watching />
      <Recommendations />
      <MoviesSection />
      <SubscribeLayout />
      <Footer />
    </div>
   );
}
 
export default MoviesRoute;