import React, { Component } from "react";
import "./App.css";

import { Provider } from "react-redux";
import store from "./store";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div>Hello dear, I'm Filba</div>
      </Provider>
    )
  }
}

export default App;
