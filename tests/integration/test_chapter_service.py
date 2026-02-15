from book_queue.models.models import Chapter
from book_queue.core.schemas import CreateChapterRequest, UpdateChapterRequest


def test_create_chapter(chapter_service, instantiate_models_and_populate_db):
    book, _, _, _, _ = instantiate_models_and_populate_db
    chapter_request: CreateChapterRequest = CreateChapterRequest(
        title='test chapter', summary='test summary', book_id=book.id
    )
    test_chapter = chapter_service.create(chapter_request)

    assert test_chapter.title == 'test chapter'


def test_get_chapter_by_id(chapter_service, instantiate_models_and_populate_db):
    _, c1, c2, _, _ = instantiate_models_and_populate_db

    chapter_in_db: Chapter = chapter_service.get_by_id(c1.id)

    assert chapter_in_db.title == c1.title
    assert chapter_in_db.id == c1.id


def test_list_chapters(chapter_service, instantiate_models_and_populate_db):
    _, c1, c2, _, _ = instantiate_models_and_populate_db
    chapters: list[Chapter] = chapter_service.list_chapters()

    assert len(chapters) == 2
    assert chapters[0].title == c1.title
    assert chapters[1].title == c2.title


def test_update_chapter(chapter_service, instantiate_models_and_populate_db):
    _, c1, _, _, _ = instantiate_models_and_populate_db

    update_data: UpdateChapterRequest = UpdateChapterRequest(
        summary='test summary'
    )

    update_chapter: Chapter = chapter_service.update(
        chapter_id=c1.id, data=update_data
    )

    assert update_chapter.summary == update_data.summary
    assert update_chapter.id == c1.id


def test_list_by_book_id(chapter_service, instantiate_models_and_populate_db):
    b1, c1, c2, _, _ = instantiate_models_and_populate_db
    chapters: list[Chapter] = chapter_service.list_by_book_id(b1.id)
    assert len(chapters) == 2
    assert chapters[0].title == c1.title
    assert chapters[1].title == c2.title


def test_get_chapter_by_note_id(
    chapter_service, instantiate_models_and_populate_db
):
    _, c1, _, n1, _ = instantiate_models_and_populate_db

    chapter_in_db: Chapter = chapter_service.get_by_note_id(n1.id)

    assert chapter_in_db.title == c1.title


def test_delete_chapter(chapter_service, instantiate_models_and_populate_db):
    _, c1, _, _, _ = instantiate_models_and_populate_db

    deleted_chapter: Chapter = chapter_service.delete(c1.id)

    assert deleted_chapter is None
