from book_queue.models.models import Note
from book_queue.schemas import CreateNoteRequest, UpdateNoteRequest


def test_create_note(note_service, instantiate_models_and_populate_db):
    _, c1, _, _, _ = instantiate_models_and_populate_db

    note_request: CreateNoteRequest = CreateNoteRequest(
        title='title',
        content='content',
        chapter_id=c1.id,
    )

    note: Note = note_service.create(note_request)

    assert note.title == 'Title'
    assert note.content == 'content'
    assert note.chapter_id == c1.id


def test_get_note_by_id(note_service, instantiate_models_and_populate_db):
    _, _, _, n1, _ = instantiate_models_and_populate_db

    note_in_db: Note = note_service.get_by_id(n1.id)

    assert note_in_db.title == n1.title
    assert note_in_db.content == n1.content


def test_delete_note(note_service, instantiate_models_and_populate_db):
    _, _, _, n1, _ = instantiate_models_and_populate_db

    deleted_note: Note = note_service.delete(n1.id)
    assert deleted_note is None


def test_update_note(note_service, instantiate_models_and_populate_db):
    _, _, _, n1, _ = instantiate_models_and_populate_db

    note_request: UpdateNoteRequest = UpdateNoteRequest(
        title='New Title',
    )
    note: Note = note_service.update(n1.id, note_request)

    assert note.title == 'New Title'
    assert note.content == n1.content


def test_list_by_chapter_id(note_service, instantiate_models_and_populate_db):
    _, c1, _, n1, _ = instantiate_models_and_populate_db

    notes_list: list[Note] = note_service.list_by_chapter_id(c1.id)

    assert len(notes_list) == 1
    assert notes_list[0].id == n1.id


def test_list_by_book_id(note_service, instantiate_models_and_populate_db):
    b1, c1, _, n1, n2 = instantiate_models_and_populate_db

    notes_list: list[Note] = note_service.list_by_book_id(b1.id)

    assert len(notes_list) ==2
    assert notes_list[0].id == n1.id
    assert notes_list[1].id == n2.id
    assert c1.notes[0] == n1
