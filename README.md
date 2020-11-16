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

`/api/choice` : getting user's genre's choice for data processing

`/api/loved/movies`: getting movies a user thumbs up

`/api/add/friend/<string:name>, method=post` : adding friend

`/api/my/friends` : list of current user's friends

`/api/create/room/for/<string:movie, method=post` : creating room for movie

`/api/watch/<string:movie>/in/room/<string:room>` : watching movie in created room

`/api/my/rooms` : list of current user's room

`/api/my/rooms/delete/<string:room_id>, method=post` : current user deleting a room

