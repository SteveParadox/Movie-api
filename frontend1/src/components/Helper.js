// Helper functions to registration, login processes, etc
import axios from "axios";
import urls from "../apiEndPoints";

export const register = async obj => {
  // const options = {
  //   "name": obj.firstName + " " + obj.lastName,
  //   "email": obj.email,
  //   "dob": obj.dob,
  //   "password": obj.password,
  //   "country": obj.country,
  //   "phone_no": obj.number
  //   // Please add the preferred genre to the list and make a special request but that should be after registration is successful.
  // };

  const res = await axios.post(urls.signup, { ...obj });
  console.log(res);
  // if res is ok, do:
    // return special made object with success = true
  if(res.status === 200 && res.statusText === "OK") {
    return {
      success: true,
      data: res.data,
    }
  }

  // else do:
    // return special object with success = false
  else {
    console.log("Sorry, Signup was not successful");
    return {
      success: false,
      data: {},
    }
  }
};

export const login = async obj => {
  const options = {
    "email": obj.email,
    "password": obj.password,
  };

  const res = axios.post(urls.login, { body: options });
  console.log(res);
  // if res is ok, do:
    // return special made object with success = true
    if(res.status === 200 && res.statusText === "OK") {
      return {
        success: true,
        data: res.data,
      }
    }
  
    // else do:
      // return special object with success = false
    else {
      console.log("Sorry, Login was not successful");
      return {
        success: false,
        data: {},
      }
    }
};

export const logout = obj => {
  axios.post(urls.logout, {})
    .then(res => {
      // Remove the already stored token from local storage
      console.log(res);
    })
}