# FSND-Capstone-Project (Casting Agency)
My Capstone Project for Full Stack NanoDegree Udacity Course.  
The project is hosted remotely on Heroku at the link: https://omar-fsnd-casting-agency.herokuapp.com/

## Project Motivation
The project is to demonstrate my understanding of all the concepts that have been taught throughout the duration of the course.  
And as quoted from the the project requirements from Udacity:
> The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Project Dependancies
The project is based on Python language and uses Flask framework.  
And it requires PostgreSQL installation for its database functionality.  
It also requires authentication and authorization through Auth0.  
The project uses Heroku as its remote hosting service.  

The main python libraries included in `requirements.txt` are:
* Flask - Python Framework for Web development
* Flask-Cors - To enable cross origin resource sharing
* Flask-Migrate - To migrate model changes to the database
* Flask-SQLAlchemy - To provide an ORM to communicate with the database
* python-jose-cryptodome - To provide a way to decode JWT tokens for authentication and authorization
* gunicorn - To host the application with gunicorn, required for hosting on Heroku

## Local Development
Please make sure you have an updated Python3 package on your machine.  
Also please make sure that you have an updated PostgreSQL installation.  

To host the project locally you can do the following:  
1. Clone the project with `git clone https://github.com/Omarb28/fsnd-capstone-project.git`
1. Create a Virtual Environment through Python with the following command `python -m venv venv`
1. Source into it using the command `source venv/bin/activate`
1. Install the required dependencies using the command `pip install requirements.txt`
1. Source the environment variables found in `setup.sh` using the command `source setup.sh`
1. Make sure that the environmental variable `DATABASE_URL` contains the correct username and password for your postgresql installation.
1. Then the model changes can be migrated with the following command `flask db upgrade` after changing the working directory to `src` folder with the command `cd src`.
2. After that, you can seed data into the database by going to the folder `src/database/` and then using the command `psql casting-agency < movie_data_seed.psql`.
3. Finally the flask API can be run with the command `flask run --host=0.0.0.0 --port=5000`.

### Authentication Setup
Tokens are provided for each role with long expiry time in the `setup.sh` file.  
If it is required to setup your own JWT tokens you may do the following:  
1. Login to the following link through Auth0: https://omar-fsnd.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=fYvohdJbrufgAsotomj0G7hcuos8f7FK&redirect_uri=https://omar-fsnd-casting-agency.herokuapp.com/
1. After logging it will redirect you to a page. You can find your JWT token in the URL in your browser after the `access_token=` attribute.
1. The JWT token can then be used to request from the API endpoints using the Authorization header with `Bearer <jwt-token>` included.

### Testing
For testing there are two ways included. First one is through Unittest library. Second one is through Postman Collection.   

* **Test with Unittest Library**  
The test file can be found at `src/test_app.py` and can be run with the command `python test_app.py`.  
Make sure that the flask API is running locally.  
Also make sure you have a test database ready so the data can be seeded then the API can be tested.  

* **Test with Postman Collection**  
The postman collection is available in the file `FSND - Final Project - Casting Agency.postman_collection.json`  
The file is updated with the latest JWT token.  
Please make sure that the {{host}} varialbe is setup so it can communicate with the same configuration as the running flask API.  
There are pre-scripts running on the postman collection folders that are used to change variables for each test and role.  


There is also one final strange issue that I have faced, which is the exception for POST endpoints for both Actors and Movies. For some reason it always gives an error whenever it is run for the first time. To fix this I have found that just removing the exception and running the application without then using the endpoint to create an actor or a movie. After doing that it works and the exception can be commented out again and it will work without issues.

## Hosting Instructions
The application is currently hosted on Heroku at the link: https://omar-fsnd-casting-agency.herokuapp.com/

The updated `Procfile` and `requirements.txt` are provided with the project. As they are required for hosting on Heroku.
And the environmental variables are provided in `setup.sh` file in the project. These have to be entered on Heroku website through Config Variables.

To be able to host the application, the following should be followed:
1. Install Heroku CLI on your machine.
1. Login to Heroku on the CLI.
1. Create a new application with a name of your choice. Using the following command:
`heroku create name_of_your_app`.
1. Add a remote heroku branch to your local repository so it can detect and deploy changes whenever pushed, using the command `git remote add heroku heroku_git_url`. The URL is provided after creating the application through the CLI.
1. Add PostgreSQL addon to your application using the following command `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
1. Next you can push the repo to Heroku using the command `git push heroku master`

Two more things are required which as well, which are to migrate the database changes, and to update the DATABASE_URL so it can work with SQLAlchemy:

* To migrate the changes. You will need to use bash remotely on the server to do the following:
```bash
heroku run bash
cd src
FLASK_APP=app.py flask db upgrade
exit
```

* The DATABASE_URL change is required because the link automatically created by Heroku starts with `postgre://` while SQLALchemy requires it to start with `postgresql://` instead.

There is also one final strange issue that I have faced, which is the exception for POST endpoints for both Actors and Movies. For some reason it always gives an error whenever it is run for the first time. To fix this I have found that just removing the exception and running the application without then using the endpoint to create an actor or a movie. After doing that it works and the exception can be commented out again and it will work without issues.

## API Documentation
The project uses JSON as communication protocol. And is built to be a RESTful API.

Following are the endpoints available:

* **Endpoint `/` with method `GET`**  
This is the root endpoint for the API. It returns a welcome message.  
It does not require any authorization to view the message.  

* **Endpoint `/actors` with method `GET`**  
This endpoint returns a list of all actors available in the database.  
It requires to be authorized to `get:actors` permission.  

* **Endpoint `/actors` with method `POST`**  
This endpoint creates a new actor in the database.  
It requires to be authorized to `post:actors` permission.  
It expects a JSON body message from the request that contains all the following attributes:  
```javascript
{
  "name": "Name of the Actor",
  "age": 30  // Age of the actor. Must be a positive Integer
  "gender": "Gender of the Actor. Must be either Male or Female"
}
```

* **Endpooint `/actors/<id>` with method `GET`**  
This endpoint returns information of the actor with the `id` requested in the URL.  
It requires to be authorized to `get:actors` permission.  
It requires an `id` to be provided in the URL.  

* **Endpoint `/actors/<id>` with method `PATCH`**  
This endpoint updates the information of the actor with the `id` requested in the URL.  
It requires to be authorized to `patch:actors` permission.  
It requires an `id` to be provided in the URL.  
It expects a JSON body message from the request that contains some or all of the following attributes:  
```javascript
{
  "name": "Name of the Actor",
  "age": 30  // Age of the actor. Must be a positive Integer
  "gender": "Gender of the Actor. Must be either Male or Female"
}
```

* **Endpoint `/actors/<id>` with method `DELETE`**  
This endpoint deletes an actor from the database.  
It requires to be authorized to `delete:actors` permission.  
It requires an `id` to be provided in the URL.  

* **Endpoint `/movies` with method `GET`**  
This endpoint returns a list of all movies available in the database.  
It requires to be authorized to `get:movies` permission.  

* **Endpoint `/movies` with method `POST`**  
This endpoint creates a new movie in the database.  
It requires to be authorized to `post:movies` permission.  
It expects a JSON body message from the request that contains all the following attributes:  
```javascript
{
  "title": "Title of the Movie",
  "release_year": 2020  // Release year of the movie. Must be a positive Integer
}
```

* **Endpooint `/movies/<id>` with method `GET`**  
This endpoint returns information of the movie with the `id` requested in the URL.  
It requires to be authorized to `get:movies` permission.  
It requires an `id` to be provided in the URL.  

* **Endpoint `/movies/<id>` with method `PATCH`**  
This endpoint updates the information of the movie with the `id` requested in the URL.  
It requires to be authorized to `patch:movies` permission.  
It requires an `id` to be provided in the URL.  
It expects a JSON body message from the request that contains some or all of the following attributes:  
```javascript
{
  "title": "Title of the Movie",
  "release_year": 2020  // Release year of the movie. Must be a positive Integer
}
```

* **Endpoint `/movies/<id>` with method `DELETE`**  
This endpoint deletes an movie from the database.  
It requires to be authorized to `delete:movies` permission.  
It requires an `id` to be provided in the URL.  


## RBAC Controls Documentation

The roles provided in this project are as follows:
1. _**Casting Assistant**_: Has basic viewing permission on Actors and Movies.
1. _**Casting Director**_: Able to view and edit Actors and Movies. Also able to add and remove Actors.
1. _**Executive Producer**_: Has full control. Able to view, edit, add, and remove both Actors and Movies.

The permissions provided are as follows:
* Actor Permissions:
  * `get:actors`
  * `post:actors`
  * `patch:actors`
  * `delete:actors`

* Movie Permissions:
  * `get:movies`
  * `post:movies`
  * `patch:movies`
  * `delete:movies`

## Conclusion
Thank you for reviewing my project. I hope that all the requirements are fulfilled.  
The project includes MIT License.
