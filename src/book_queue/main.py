from contextlib import asynccontextmanager

from fastapi import FastAPI

from book_queue.api.v1 import books

app = FastAPI()
app.include_router(books.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}
