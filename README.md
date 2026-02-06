# Book Queue

- My aim is for this to be the back-end for an a small blog-like website in which i plan to publish notes on techinical
  books and topics that i am currently studying.
- I also aim to use TDD for this project, but i will be pragmatic about it(might not have a lot or any unit test, since
  models are mapped direct to the database.

> front-end will be in a separate repo but it will be in react (link will be added later in future)

## Intended Project architecture

- I plan to use layered architecture during the development of this application, having layers as follows:
    - Presentation layer;
    - Business logic layer - models;
    - Data access layer;
  > _orm models and business rules will be in the same layer for the sake of simplicity_

## Stack

- FastAPI for the presentation layer
- SQLAlchemy for orm mapping;
- still deciding on databases (Postgres/ Mysql);

### Notes

- im really inclined towards flask but i have 3 years of experience with FastAPI;
- really inclined towards Postgres as i don't have a lot of familiarity with it;
