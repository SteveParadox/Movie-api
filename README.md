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

`/api/choice`: getting movie based on user's registered genre

`/api/loved/movies`: getting movie based on movies a user likes

`/api/user/profile` : user profile

`/api/upload/story, method=post`: current_user uploading a story

`/api/user/story`: getting current user's story

`/api/my/friend/<string:name>/suggest`: suggesting movies a user and his friend would like based on registered genre