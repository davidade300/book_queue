from sqlalchemy.orm import Session

from book_queue.core.schemas import (
    CreateNoteRequest,
    NoteResponse,
    NoteResponseList,
    UpdateNoteRequest,
)
from book_queue.models.models import Book, Chapter, Note
from book_queue.services.notes_service import NoteService


def test_create_note(test_client, note_request: CreateNoteRequest):
    response = test_client.post(
        '/notes', json=note_request.model_dump(mode='json')
    )
    json_note: NoteResponse = NoteResponse.model_validate(response.json())

    assert response.status_code == 201
    assert (
        json_note.id == 3
    )  # two notes are created in the note_request fixture


def test_delete_note(
    test_client, note_request: CreateNoteRequest, db_session: Session
):
    note: Note = NoteService(db_session).create(note_request)
    response = test_client.delete(f'/notes/{note.id}')

    assert response.status_code == 204


def test_get_note_by_id(
    test_client, note_request: CreateNoteRequest, db_session: Session
):
    note: Note = NoteService(db_session).create(note_request)
    response = test_client.get(f'/notes/{note.id}')

    json_note: NoteResponse = NoteResponse.model_validate(response.json())

    assert response.status_code == 200
    assert note.id == json_note.id


def test_list_note_by_book_id(
    test_client,
    instantiate_models_and_populate_db: tuple[
        Book, Chapter, Chapter, Note, Note
    ],
):
    book, _, _, n1, n2 = instantiate_models_and_populate_db

    response = test_client.get(f'/notes/by_book/{book.id}')

    json_notes: NoteResponseList = NoteResponseList.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert json_notes.notes[0].id == n1.id
    assert json_notes.notes[1].id == n2.id


def test_list_note_by_chapter_id(
    test_client,
    instantiate_models_and_populate_db: tuple[
        Book, Chapter, Chapter, Note, Note
    ],
):
    _, chapter, _, n1, _ = instantiate_models_and_populate_db

    response = test_client.get(f'/notes/by_chapter/{chapter.id}')

    json_notes: NoteResponseList = NoteResponseList.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert json_notes.notes[0].id == n1.id


def test_update_note(
    test_client, note_request: CreateNoteRequest, db_session: Session
):
    note_service: NoteService = NoteService(db_session)
    note: Note = note_service.create(note_request)

    update_data: UpdateNoteRequest = UpdateNoteRequest(
        title='updated title',
        content='updated content',
    )

    response = test_client.patch(
        f'/notes/{note.id}', json=update_data.model_dump(mode='json')
    )

    updated_note: NoteResponse = NoteResponse.model_validate(response.json())

    assert response.status_code == 200
    assert updated_note.id == note.id
    assert updated_note == NoteResponse.model_validate(note)
