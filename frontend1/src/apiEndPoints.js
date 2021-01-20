const urls = {
  trending: "https://movie-stream-api.herokuapp.com/api/trending",
  popular: "https://movie-stream-api.herokuapp.com/api/popular",
  all: "https://movie-stream-api.herokuapp.com/api/",
  search: "https://movie-stream-api.herokuapp.com/api/search/movie",
  img: "https://res.cloudinary.com/du05mneox/image/upload/",
  signup: "https://movie-stream-api.herokuapp.com/api/sign_up", // POST request
  login: "https://movie-stream-api.herokuapp.com/api/login", // GET request, With Body
  logout: "https://movie-stream-api.herokuapp.com/api/logout", // POST request, No Body
  selectGenre: "https://movie-stream-api.herokuapp.com/api/select/genre", // POST request, Create a special route for selecting the genres.
};

export default urls;