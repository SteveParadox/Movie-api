import React, {
  useState,
  createContext
} from "react";

export const MovieContext = createContext();

export const MovieProvider = (props) => {
  const [appState, setAppState] = useState({
    friendsDisplay: false,
    detailsDisplay: false,
    logged_in: false,
    user_name: "",
    details: {
      top: 0,
      left: 0,
      ui_id: "",
      title: "",
      desc: "",
      genre: "",
      rating: "",
      director: "",
      year: ""
    }
  });
  return (
    <MovieContext.Provider value = {[appState, setAppState]} >
      {props.children}
    </MovieContext.Provider>
  );
}