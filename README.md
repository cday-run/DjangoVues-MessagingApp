#Project Description

This project is meant to be a chat/messaging application is which users can create or join chat rooms to converse in.  By creating an account
or logging in users will have the option to create a chatroom, or via copying and pasting a link to a currently active chatroom into the browser url bar, join a chat room.  Once in the room users can send and recieve messages in real time.  User messages appear on the right in green and other room member's messages appear on the left.

#Back-end
On the back-end this project uses the Django framework.  Specifically, it utilizes the Django-REST api fromaework and Djoser libraries to handle database managment and user authentication.  To handle the realtime messanging it utilizes websockets with uWSGI, Celery as the worker, and RabbitMQ.

#Front-end
For the front-end design, the project uses the Vue.js framework.  Vue.js was used over plain JS to allow for better state management, and was used over React.js as to experiment with other JS frameworks.

#What is Contained in Each Directory
1. env
- This is the folder that contains development environment and its packages

2. messenger (Django Project Folder)
- manage.py
- websocket.py
- dc.sqlite3

3. messenger/core (Django Application Folder)
- migrations
- admin.py
- channels.py
- models.py
- tests.py
- urls.py
- views.py

4. messenger/messenger
- asgi.py
- celery.py
- settings.py
- urls.py
- wsgi.py

5. messenger/messenger-frontend (Vue.js Folder)
- build
- config
- src
	1. assests
		- hourglass.png
		- logo.png
	2. components
		- Chat.vue
		- UserAuth.vue
	3. router
		- index.js
		- App.vue
		- main.js
- static
- test
- .babelrc
- .editorconfig
- .eslintrc.js
- .gitignore
- .postcssrc.js
- index.html
- package-lock.json
- package.json
- README.md

#Why This Project Satisfies Requirements
This project is significantly distinct from other projects in the class as it utilizes websockets, a topic that was not covered in the course.  Additionally, it expands on the topic of asyncronous updates from project 4, but uses them in the context of a real-time messaging application.  None of the other projects in the course were to design a messaging like application.  This project continues to expand on asyncronous update methods by moving beyond the JavaScript 'fetch' server communication method learned in class, and implements Axios' ajax methods to communicate with the server.  The project also incorporates a JavaScript framework not used in the course in the form of Vue.js.

The complexity requirment is met through this project as it required constructing a Django back-end, a JavaScript front-end, and a third-party distributed task queue worker (in the form of Celery) to manage the websockets.  These three components of the project then had to be connected together such that the messaging could occur in real-time, and multiple chat rooms with different users can exist at the same time.  The local application then needed to be linked to the RabbitMQ cloud based message broker to manage the Message Queuing Protocal.


Furthermore, as was required, this application uses the Django framework on the back-end and JavaScript(in the for of the Vue.js framework) on the front-end.  

#Additional Information
1. References:
- Reference on RabbitMQ here: https://www.rabbitmq.com/
- Reference on Celery here: https://docs.celeryproject.org/en/stable/index.html
- Reference on uWSGI here: https://uwsgi-docs.readthedocs.io/en/latest/#
- Reference on Axios here: https://github.com/axios/axios
- Reference on Djoser here: https://djoser.readthedocs.io/en/latest/
- Reference on Django REST Framework here: https://www.django-rest-framework.org/
- Reference on Vue.js here: https://vuejs.org/
- HTML template source: Osaetin Daniel

2. Notes:
- I decided to try and use Celery and RabbitMQ over Django Channels (though it may have been more straightforward for this project) to manage the websockets for the project, as I thought it would be interesting to learn methods outside of Django for managing websockets in the future, incase I decide to build an application that does not use Django on the back-end.

3. Console Commands:
- sudo systemctl start rabbitmq-server
- celery -A messenger worker -l info
- uwsgi --http :8081 --gevent 4 --module websocket --gevent-monkey-patch --master
- python3 manage.py runserver
- npm run dev
