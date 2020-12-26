# FILBA
- Front-end Framework: **React, React-dom**
- Front-end Ajax communication: **axios, socket.io-client**
- Front-end Web RWD Design:
- Back-end: **Python-Flask**
- Database: **SQLITE, POSTGRESQL**
- Bundle: 


# Back-end

##Hosted on:
```
$ movie-stream-api.herokuapp.com
```

**fetching images from storage**
```
$ <img src="https://res.cloudinary.com/dc1qkmsr0/image/upload/{{movie name}}.jpg"
```
**fetching movies from storage**
```
$ <video poster="https://res.cloudinary.com/dc1qkmsr0/video/upload/{{movie name}}.jpg">
 <source src="https://res.cloudinary.com/dc1qkmsr0/video/upload/{{movie name}}" type="video/webm"/>
  <source src="https://res.cloudinary.com/dc1qkmsr0/video/upload/{{movie name}}" type="video/mp4"/>
  <source src="https://res.cloudinary.com/dc1qkmsr0/video/upload/{{movie name}}" type="video/ogg"/>
</video>

```
**Note**
```
$ All data fetched from the storage must be in the database except it returns empty
$ Database tables can be found in models.py
$ movie name is the name of the movie in database
```



**Routes**

`/api/sign_up, method=post` : create account

`/api/login` : login to app

`/api/select/genre, method=post` : register preferred movie genres

`/api/logout, method=post` : logout from app

`/api/` : Home page

`/api/search/movie` : search for movie

`/api/get/movie/<string:u_id>/` : route to selected movie

`/api/genre/<string:genre>` : getting movies of an individual genre 

`/api/similar/movie/<string:u_id>`: getting similar movies to a currently viewed movie

`/api/like/movie/<string:u_id>, method=post` : thumbs up a movie

`/api/dislike/movie/<string:u_id>, method=post` : thumbs down a movie

`/api/add/friend/<string:name>, method=post` : adding friend

`/api/my/friends` : list of current user's friends

`/api/create/room/for/<string:movie>, method=post` : creating room for movie

`/api/watch/<string:movie>/in/room/<string:room>` : watching movie in created room

`/api/my/rooms` : list of current user's room

`/api/my/rooms/delete/<string:room_id>, method=post` : current user deleting a room

`/api/choice`: getting movie based on user's registered genre

`/api/loved/movies`: getting movie based on movies a user likes

`/api/user/profile` : user profile

`/api/upload/story, method=post`: current_user uploading a story

`/api/user/story`: getting current user's story

`/api/friend/story`: list of current user's friend's story

`/api/my/friend/<string:name>/suggest`: suggesting movies a user and his friend would like based on registered genre

`/api/popular`: getting popular movies

`/api/trending`: getting trending movies

`/api/add/list/<string:movie_id> method=post`: add a movie to current_user's watchlist

`/api/my/list`: list of all current user's stored movies



# Socket Routes

**on**
```hgignore
$ send_invite: host of the room invites friends
```
**emits**
```hgignore
$ Invited: 'data' the link of the room, the host 'name' and 'movie' watched in the room
```

**on**
```
$ join_user: gets the room id and adds the invited user to the room
```
**emits**
Nothing

**on**
```
$ group_message: getting the 'name', 'room_id' and 'message' a user typed
```

**emits**
```
$ New_group_Message: An alert 'message' to the members of the room 
```
**emits**
```
$ New: sends the 'sender' of the message, 'time' message was sent, message 'data' that was sent
```
