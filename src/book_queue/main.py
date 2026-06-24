import uvicorn
from fastapi import FastAPI

from book_queue.api.v1 import books, chapters, notes, auth
from book_queue.core.database import engine
from book_queue.models.models import Base

app = FastAPI()
app.include_router(books.router)
app.include_router(chapters.router)
app.include_router(notes.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.get('/before_all')  # Todo: REMOVE THIS BEFORE DEPLOY
def before_all():
    Base.metadata.create_all(engine)
    return {'Tables': 'Created'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
