import React from 'react';

// Import components
import AppNavBar from "./AppNavBar";
import Banner from "./TestBanner";
import Watching from "./Watching";
import Recommendations from "./Recommendations";
import SubscribeLayout from "./SubscribeLayout";
import Footer from "./Footer";

const MoviesSection = (props) => {
  return ( 
    <div className="mvpage">
      <AppNavBar />
      <Banner />
      <Watching />
      <Recommendations />
      <SubscribeLayout />
      <Footer />
    </div>
   );
}
 
export default MoviesSection;