from fastapi import FastAPI

from book_queue.api.v1 import books, chapters
from book_queue.core.database import engine
from book_queue.models.models import Base

app = FastAPI()
app.include_router(books.router)
app.include_router(chapters.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.get('/before_all')  # Todo: REMOVE THIS BEFORE DEPLOY
def befora_all():
    Base.metadata.create_all(engine)
    return {'Tables': 'Created'}
