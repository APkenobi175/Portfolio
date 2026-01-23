# Module 1

### IP Addresses
	* 8-27-25.md
	* An IP Address identifies a machine on a network
	* Its an address used by routers to deliver packets
	* Localhost = 127.0.0.1

### Ports
	* 8-27-25.md
	* Differenciates services on an IP
	* HTTP = Port 80
	* HTTPS = Port 443
	* SSH = Port 22

### TCP / UDP
	* 9-5-25.md/9-4-25.md
	* TCP is a protocol that establishes a connected before sending data. Its slower but ensures that all the packets are delivered
		* Transmission Control Protocl
	* UDP is a protocol that just sends packets and doesn't need an established connection. It is faster but not as secure
		* User Datagram Protocol
### HTTP
	* Please see 9-7-25.md and 9-5-25.md for more in depth notes
	* Protocol over TCP. Has requests and responses that have:
		* Startline, Headers, Blank Line, Body
		* Example:
			```
			GET /index.html HTTP/1.1
			Host: example.com
			```
		* Example Response:
			```
			HTTP/1.1 200 OK
			Content Type: blablabla
			```
	* Methods
		* GET - Read
		* POST - create/process data
		* PUT - Replace
		* DELETE - remove stuff

	* Status Codes
		* 2xx = success (200 OK, 201 Created, etc)
		* 3xx = redirect (301,302)
		* 4xx = error (400 Bad request, 401 Unauthorized, 403 Forbidden, 404 Not found, etc)
		* 5xx = Server error (500)

### Advanced Python
	* Please see 9-6-25.md for more in depth notes
	* Higher Order Functions
		* Functions that take other functions as arguments or return functions
		* This is how the middleware works

	* Virtual Enviroments
		* Used to isolate dependancies to prevent conflicts in versions between projects
		* How to use Poetry (Use 9-8-25.md as a reference)
		```
		Create a folder for your project to live in.
		Initialize poetry in that folder: poetry init
		Add Django: poetry add Django
		Create a Django project: django-admin startproject <project name> replace <project name> with the name of your project
		Change the directory into your project directory (the one with manage.py)
		Create an app: python manage.py startapp <appname>
		Open up your projects settings.py file and remove all of the apps except the staticfiles and contenttype apps from the INSTALLED_APPS list.
		Also, remove the auth and messages context processors from the TEMPLATES array
		Add your app to the INSTALLED_APPS list
		Remove all of the middleware except the clickjacking, security, and common middleware.
		Remove the admin URLs from the project's urls.py file.
		Create a urls.py file in your app. Add the following content to it:

		from django.urls import path
		from . import views
		urlpatterns = [
			    # put your paths here
			        (looks like 
			            urlpatterns = [
			            	    path('', views.index, name='index'),
			            	        path('passwords/', views.passwords, name='passwords'),
			            	        ])
			            	        ]
			            	        Include your app's URLs in the project's urls.py file.

			            	        Build your app! 

			            	        ```
			            	        * Don't forget in the projects URL files do this
			            	        ```python
			            	        from django.urls import include
			            	        urlpatterns = [
			            	        	    path("", include ("core.urls") ),
			            	        	    ]
			            	        ```

	* Middleware
		* Handle everything that happens before/after your views. basically the middle man that processes requests
		* Examples:
			* Authentication
			* Logging

# MODULE 2


### Django
	* Please see 9-8-25.md for more in depth notes
	* 9-10-25.md can also be useful
	* Django Commands you Need to know:
		1. django-admin startproject name 
			* Starts a project
		2. python manage.py startapp core
			* Starts your app
		3. python manage.py makemigrations
			* Gets your migrations all ready
		4. python manage.py migrate
			* actually migrates your data and updates/creates the database
		5. python manage.py runserver
			* Starts an HTTP server for your application
		6. Please see above notes on how to properly start a Django project (or check 9-8-25.md)
	* Django Template Syntax
		* { / %        % / } and such
	* Configuring App
		* See above notes, and also add your app to INSTALLED_APPS in settings.py
		* Don't forget to add the URLS like this:
		```
		from django.urls import path, include
		 urlpatterns=[path("", include("core.urls"))]
		```
		* To load your static files do this at the beginning of your html
		```
		{ / % Load Static % / }
		```
		* and
		```
		<link rel = "stylesheet" href="{% static 'core/style.css' %}"
		```
		* Variables in html
		```
		{ / { variable } / }
		```
	* CRSF TOken
		* In forms a crsf token is required
		* CRSF means Cross Site Request Forgery. THis makes sure your CRSF token is correct when submitting a form so we know the right user is submitting it
		* A button inside a form automatically submits the form

### Forms in HTML

	* Your input elements should have **names** — they act as variable identifiers.

	```
	[14/Sep/2025 21:51:27] "GET /passwords/?length=12&count=5 HTTP/1.1" 200 4
	```

	* When you submit a form, you can see the query parameters in the GET request.
	* You can also make a POST request with the same information:

	```html
	<form action="/passwords/" method="post">
	```

	* You can retrieve information from GET or POST requests using `request.GET` or `request.POST`.

	Example:

	```python
		from django.http import HttpRequest, HttpResponse

		def passwords(request: HttpRequest):
    		query = request.GET
        	print(query.get("length", 1))
            print(query.get("count", 1))  # Using .get prevents KeyError and allows default values
            return HttpResponse("TEST")
    ```

    * Everything from a request is a **string**, so if you need numeric values, convert them using `int()`.

### MVC Design Pattern
	* See 9-14-25.md for more in depth notes 
	* Componenets of MCV:
		* Controller
		* Model
		* View
	* Django Version
		* Controller = View - Interacts with the Models
		* Model = Model - Things the application works with
		* View = Template - Your endpoints I think

### RESTFul Routing
	* See 9-19-25.md for more in depth notes
	* Basically REST is CRUD for HTTP
### CRUD in Djagno
	* You can do CRUD with SQL
	* OR you can use Django functions
		* Create
			* post.objects.create(balabfsd = "fdsf", fsd = "fdsfsd")
		* Read
			* Post.objects.all(), post.objects.get(pk=1) (Primary key =1, first element in table)
		* Update
			* q = post.objects.get(pk=1), get the data first
			* q.title = "New stuff"
			* p.save()
		* Delete
			* q.delete()
### Relationships In Django
	* See 9-20-25.md for more in depth notes
	* One to One
		* models.OneToOneField
		* Two Fields are related to each other
	* One To Many
		* models.foreignKey
		* One course, can have many assignments
		* on_delete=models.CASCADE means if the course is deleted the assignments will be deleted too
	* Many To Many
		* Requires a bridge table in the middle
		* models.ManyToManyField
### Database
	* See 9-26-25.md for more in depth notes on SQL and Databse operations

### Other Useful things you might need (9-27-25.md)
* MVC stands for Model View Controller
	* Model - Manages the data and business logic
		* View - Handles how information is displayed to user
			* Controller - Manages input, converting it to commands for the model or view

			* Models are the things your application deals with.  
			* All models have an ID attribute
			* Restful Routing, the two key pieces of information used to identify the resource are method and URI
			* A foreign key contraint ensures that the value in a column references a valid primary key of a row in another table

			* ORM Stands for Object-Relational Mapping
				* ORM is the technique used that lets you work with a database using objects in your programming language instead of writing raw SQL


					
	
