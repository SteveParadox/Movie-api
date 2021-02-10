import React, { useEffect, useState } from 'react';
import { Redirect } from "react-router-dom";
import axios from "axios";
import urls from "../apiEndPoints";

const RouteProtect = (props) => {
  const [logged_in, setLogged] = useState(false);

  useEffect(() => {
    console.log("Choice");
    const getLogged_State = () => {
      axios.get(urls.all)
        .then(res => {
          console.log(res);
          setLogged(res.data["logged in"]);
        })
        .catch(() => console.log("Something went wrong!"));
    };
    getLogged_State();
  }, [setLogged]);

  return (
    <>
      {logged_in ? <Redirect to={{pathname: "/signin", state: props.to}} /> : null}
    </>
  );
};

export default RouteProtect;