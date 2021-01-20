import React from "react";

// The components
import AppNavBar from "./AppNavBar";
import Banner from "./TestBanner";
import Watching from "./Watching";
import Recommendations from "./Recommendations";
import Movies from "./Movies";
import SubscribeLayout from "./SubscribeLayout";
import Footer from "./Footer";

function Home() {
  return (
    <div>
      {/* Please Note That The Recommedations Component still imposes a problem and needs urgent attention. */}
      <AppNavBar />
      <Banner />
      <Watching />
      <Recommendations />
      <Movies />
      <SubscribeLayout />
      <Footer />
    </div>
  );
}

export default Home;