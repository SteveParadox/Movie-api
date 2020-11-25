# Movie Api

**Routes**

`/api/sign_up, method=post` : create account

`/api/login` : login to app

`/api/select/genre, method=post` : select preferred movie genres

`/api/logout, method=post` : logout from app

`/api/` : Home page

`/api/search/movie` : search for movie

`/api/get/movie/<string:u_id>/` : route to selected movie

`/api/like/movie/<string:u_id>, method=post` : thumbs up a movie

`/api/dislike/movie/<string:u_id>, method=post` : thumbs down a movie


`/api/add/friend/<string:name>, method=post` : adding friend

`/api/my/friends` : list of current user's friends

`/api/create/room/for/<string:movie, method=post` : creating room for movie

`/api/watch/<string:movie>/in/room/<string:room>` : watching movie in created room

`/api/my/rooms` : list of current user's room

`/api/my/rooms/delete/<string:room_id>, method=post` : current user deleting a room

`/api/choice`: getting/analysing movies based on user's registered genre

`/api/loved/movies`: getting/analysing  movie based on movies a user likes

`/api/user/profile` : user profile

`/api/upload/story, method=post`: current_user uploading a story

`/api/user/story`: getting current user's story

`/api/friend/story`: list of current user's friend's story

`/api/my/friend/<string:name>/suggest`: suggesting movies a user and his friend would like based on registered genre

`/api/popular`: getting popular movies

`/api/add/list/<string:movie_id> method=post`: add a movie to current_user's local list for later

`/api/my/list`: list of all current user's locally stored movies

`/api/action`: list of all action movies

`/api/comedy`: list of all comedy movies

`/api/horror`: list of all horror movies

`/api/documentary`: list of all documentary movies

`/api/thriller`: list of all thriller movies

`/api/crime`: list of all crime movies

`/api/animation`: list of all animation movies

`/api/erotic`: list of all erotic movies

`/api/romance`: list of all romance movies

`/api/mystery`: list of all mystery movies

`/api/fantasy`: list of all fantasy movies

`/api/sci-fi`: list of all science fiction movies

`/api/children`: list of all children movies

