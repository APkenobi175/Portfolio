# Final Project Proposal 

Ammon Phipps

## Overview
I want to build an application for logging Astrophotography Sessions, and sharing completed images on the web. 

### Main Idea

* Users will go out at night, shoot a target, and then come to the app and log their session
* Each session will store things like the number of subs, exposure time, camera settings, location. Users will have the option to share their final stacked photo (if they have it) to the feed. 
* A session can be public or private

## Features

### Must Have Features
1. As a user, I should be able to register and log into an account
2. As a user, I should be able to see a list of my own astrophotagraphy sessions after logging in
3. As a user, I should be able to create a new session log that includes:
    * A title (target?)
    * Data and Time
    * Location (With a checkbox on whether this info is public to others or not)
    * Number of light frames
    * Exposure length per frame with support for multiple exposure times
    * ISO / Gain
    * Camera Model
    * Telescope/Lens used
    * Pixel Size (optional)
    * Number of dark frames
    * Exposure length per dark frame with support for multiple exposure times
    * Number of flat frames
    * Notes/Comments
    * A checkbox that denotes the whole session as public or private
4. As a user, I should be able to view details of a single session, with these statistics:
    * Total Integration(Exposure) Time added up from all frames
    * Average exposure time on light frames
    * Ratio of calibration frames
    * A one sentence session summary like this:
        * "3 Hours at 800 ISO with Nikon D5600 and Celestron 130SLT Telescope"
    * Total length of time for session
5. As a user I should be able to edit my past sessions, and those statistics will update as well if applicable
6. As a user, I should be able to have a feed of images or sessions from other users including their gear and camera settings

### Nice to have features:
1. As a user, I should be able to search public sessions by target
2. As a user, I should be able to filter my feed by target, time posted, camera, anything
3. As a user, additional metrics will be recorded to my log such as moon phase, elevation, etc that will be automatically calculated
4. As a user I should have a statistics page on my profile that will show me a graph of my total integration time 
5. As a user, It would be nice to have the ability to save gear configurations so I don't need to enter the same gear every time I log a session
6. As a user, I should be able to like other user's public sessions and see a list of all my liked sessions
7. As a user I should be able to see my own profile

### Technical Challenges:
1. File uploads/Storage
    * I would need to figure out how to manage users uploading photos to the site
    * I think I would want the images to remain local just for the project
    * I would need to consider file size limits so the user can't upload something insanely massive. Maybe limit the posts to .jpg or .png too so they don't upload RAW files (Those are huge)

2. Having multiple sessions, accounts, and posts
    * This should be similar to an earlier assignment we did with the location reviews, and with that the public/private posts, feed, and logging in/out should be similar

3. Filtering posts
    * This should be pretty straight forwards I can use Django to search through things in the database similar to a SQL query
    ```sql
    select * from session where ISO = ?
    ``` 
    * Something like that, but with django it would be like
    ```python
    sessions = Session.objects.filter(ISO = isoValue)
    ```
    * Filtering multiple items at the same time should be really fun to do

4. RESTful routing with Django
    * Users should only be able to see their own sessions, or public sessions
    * if a user is not logged in and tries to access their profile or sessions they should be redirected to the login page

### Requirements

1. You should build a single-page application using React with Django as the backend.
    * The frontend will be a single-page React applicction
    * Django will be the backend and use Sessions, handle authentication, do all database operations.

2. Your app should be multiple pages (using client-side routing)
    * The application will have multiple pages uses client side routings. Possible routes include:
      * /login - Login page
      * /sessions - List of users sessions
      * /sessions/new - create a new session
      * sessions/:Id - a view of a single session based on ID with all its stats
      * /sessions/:Id/edit - edit page of a single session based on it's ID
      * /public - all public sessions/posts
      * /profile (if I end up doing this) - the user's profile page


3. Your app should require authentication (this is given to you in the starter code)
    * The user must be logged in to see it's own sessions, create a session, or like a session
4. Your app must be useful (What I mean by this is that the app must be more than the sum of its parts. The app should attempt to solve a specific problem.)

    * The app will be used to track and log astrophotraphy sessions (one of my hobbies) and calculate statistics

5. Your app should have a consistent, intentional design.
    * There will be a consistent, functional design in the apps layout and pages. 
    * Dark theme to fit the astrophotraphy vibe
6. Your app must use the backend and the database in a meaningful way.
    * The database will store all the session details and statistics

### Group Members

* Just me, Ammon Phipps
* A02329446