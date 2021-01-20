import React, { useState, createContext } from "react";

export const MovieContext = createContext();

export const MovieProvider = (props) => {
  const [appState, setAppState] = useState({
    friendsDisplay: false,
  });
  return (
    <MovieContext.Provider value={[appState, setAppState]}>
      {props.children}
    </MovieContext.Provider>
  );
}