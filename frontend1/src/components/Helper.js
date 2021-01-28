// Helper functions to registration, login processes, etc
import axios from "axios";
import urls from "../apiEndPoints";

export const register = async obj => {
  try {
    const res = await axios.post(urls.signup, {
      ...obj
    });
    console.log(res);
  } catch {
    console.log("Sorry, Signup was not successful");
  }
  // return to login page
};

export const login = async obj => {
  const options = {
    "email": obj.email,
    "password": obj.password,
  };

  try {
    const res = await axios.post(urls.login, options)
    console.log(res);
  
  } catch {
    console.log("Something went wrong");
  }
  
  // Now redirect to user page.
  // make sure to set AppState's logged_in to true 
  // return;
};

export const logout = async () => {
  try {
    const res = axios.post(urls.logout)
    console.log(res);
  } catch {
    console.log("Something went wrong");
  }

  // Now redirect to login page
  // Make sure to set appState's logged_in to false
  return;
}

// Add a friend
export const AddFriend = async (friendName) => {
  let success = false;
  try {
    const res = await axios.post(`https://movie-stream-api.herokuapp.com/api/add/friend/${friendName}`);
    console.log(res);
    // if successful then
    // success = true;
  } catch(err) {
    console.log(err);
  }
  return success;
}

// Get similar movie
export const GetSimilarMovies = async (u_id) => {
  let similarMovies = [];
  try {
    const res = axios.get(`https://movie-stream-api.herokuapp.com/api/similar/movie/${u_id}`);
    console.log(res);
    // set the value of similarMovies variable to the response
  } catch(err) {
    console.log(err);
  }
  return similarMovies;
};

