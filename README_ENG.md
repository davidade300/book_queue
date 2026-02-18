# Book Queue

- My aim is for this to be the back-end for an a small blog-like website in which i plan to publish notes on techinical
  books and topics that i am currently studying.
- I using TDD for this project, but i will be pragmatic about it(might not have a lot or any unit test, since
  models are mapped direct to the database.

> front-end will be in a separate repo but it will be in react (link will be added later in future)

## Project architecture

- I'm using a layered architecture during the development of this application, having layers as follows:
    - Presentation layer -> the api itself;
    - Business logic layer ->  they are actually in the services;
    - Data access layer -> the models (which are coupled to the dabatase through the orm);

## Stack

- FastAPI for the presentation layer
- SQLAlchemy for orm mapping;
- PostgreSQL for the database;
- Pytest for testing;
- Alembic for database migrations 
