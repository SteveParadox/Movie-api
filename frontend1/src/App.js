import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./App.css";

import { MovieProvider } from "./MovieContext";
import Home from "./components/Home";
import MoviesSection from "./components/MoviesSection";
import Signin from "./components/Signin";
import Signup from "./components/Signup";
import NotFoundPage from "./components/NotFound";

class App extends Component {
  render() {
    return (
      <MovieProvider>
        <Router>
          <div className="App">
            <Route path="/" exact={true} component={Home} />
            <Switch>
              <Route path="/movies" exact={true} component={MoviesSection} />
              <Route path="/signin" exact={true} component={Signin} />
              <Route path="/signup" exact={true} component={Signup} />
              <Route path="/:unknown" exact={true} component={NotFoundPage} />
            </Switch>
          </div>
        </Router>
      </MovieProvider>
    );
  }
}

export default App;
