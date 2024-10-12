# Anime Finder
#### Video Demo: https://www.youtube.com/watch?v=SdZz5_UWexc
#### Description:
This is a web application that lets you find an anime through an image from it, it shows you which anime it is and which episode the image is taken from, It uses trace.Moe API to find it and it takes the information and conveys it to the user.

Though i struggle a bit in the uploading images part i figure a way to work around that by making the user upload the image to an image hosting site the webpage could access it through the web using a url thus not needing to upload it.

There is also a sign up feature that lets you view the history of your searches by first checking if the a user is signed in then saving the result in a history table using SQL and you can reaccess the results from the history page.

I used a navigation bar from bootstrap which uses javascript to collapse if the screen width isn't big enough and it turns into a dropdown menu.

first, layout.html contains the navigation bar of the page with the logo and at the bottom it has credit for the api I am using, I used the idea from finance to make the navigation bar different depending on if the user is signed in or not.

index.html has the a simple description of what the website does and an image that signifies screenshot.

find.html has a form that takes an image url and after submiting it renders found.html that has the info about the anime from the image just submited, if the user is signed in it saves the result in the history table in project.db, if not signed in it skips this part and just shows the result without saving.

history.html you need to be signed in to access using the login_required function from finance, It goes inside the history table and looks for all the rows with the same user_id from the session and shows the past results with the date of the search and two buttons to either view that result again or to remove from history.

login.html and register.html don't have anything new it just the same as in finance.

now app.py, first i got the starting stuff from finance,

route"/" just renders index.html, the main page.

route"/login" does the same as in finance it clears the session and if accessed through get it renders login.html, if through post it checks the input the signs the user in and redirects to "/" the main page.

route"/register" it's pretty much the same as login it just takes confirmation and inserts the user info into project.db and signs user in and redirects to "/".

route"/logout" just clears session and redirects to "/".

route"/find" is the most i struggled with, first i tried to make an upload file input in the form for post but i couldn't figure out how to access the image and i had to save it somewhere and then delete it after and i just couldn't get it to work, so instead i figured i should make the user host the image online and then paste the url to the image so that the website can access that image without the hassle of downloading it, it asks the api with that image and then the api returns a bunch of data and i give that data to found.html,
It also check if the field is empty and if the url isn't an image, then if the session is not empty it saves the result to the user.

route"/found" is accessed through the view button in the history page, it takes the image in the history table and asks the api for the info again with the image and renders found.html with that data.

route"/history" requires logging in it takes the name of the user and takes all the results saved in history with that name and sends it to history.html.

route"/remove" does not have a page, it's a button in history (a form) it takes the id of that row in the history table and deletes it then redirect the user back to history.

project.db has two tables users and history, users has the user data for logins and history has the result history with usernames for each row to be accessable per user.

in static there an Image folder, it has the logo image and the background pattern and the screenshot "symbol" for the main page.

styles.css has some random css for some stuff for the table in history.

helpers.py has some of the functions from finance that i took.