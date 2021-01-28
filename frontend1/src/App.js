import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./App.css";

import { MovieProvider } from "./MovieContext";
import Home from "./components/Home";
import User from "./components/User";
import Watch from "./components/Watch";
import MoviesRoute from "./components/MoviesRoute";
import Signin from "./components/Signin";
import Signup from "./components/Signup";
import NotFoundPage from "./components/NotFound";

class App extends Component {
  render() {
    return (
      <MovieProvider>
        <Router>
          <div className="App">
            <Switch>
              <Route path="/" exact={true} component={Home} />
              <Route path="/watch/:movie_id" exact={true} component={Watch} />
              <Route path="/user" exact={true} component={User} />
              <Route path="/movies" exact={true} component={MoviesRoute} />
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
