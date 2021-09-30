# fsnd-capstone-project (Casting Agency)
My Capstone Project for Full Stack NanoDegree Udacity Course.  
The project is hosted remotely on Heroku at the link: https://omar-fsnd-casting-agency.herokuapp.com/

## Project Motivation
The project is to demonstrate my understanding of all the concepts that have been taught throughout the duration of the course.

## Project Dependancies


## Local Development


## Hosting Instructions


## API Documentation
The project uses JSON as communication protocol. And is built to be a RESTful API.

Following are the endpoints available:

* Endpoint `/` with method `GET`  
This is the root endpoint for the API. It returns a welcome message.  
It does not require any authorization to view the message.

* Endpoint `/actors` with method `GET`  
This endpoint returns a list of all actors available in the database.  
It requires to be authorized to `get:actors` permission.

* Endpoint `/actors` with method `POST`
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

* Endpooint `/actors/<id>` with method `GET`  
This endpoint returns information of the actor with the `id` requested in the URL.
It requires to be authorized to `get:actors` permission.
It requires an `id` to be provided in the URL.

* Endpoint `/actors/<id>` with method `PATCH`  
This endpoint updates the information of the actor with the `id` requested in the URL.  
It requires to be authorized to `patch:actors` permission.
It requires an `id` to be provided in the URL.
It expects a JSON body message from the request that contain

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
Thank you for reviewing my project. Hope I did not miss any requirement.
