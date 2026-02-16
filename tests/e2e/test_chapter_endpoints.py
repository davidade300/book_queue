from sqlalchemy.orm import Session

from book_queue.core.schemas import (
    ChapterResponse,
    ChapterResponseList,
    CreateChapterRequest,
)
from book_queue.models.models import Book, Chapter, Note
from book_queue.services.chapter_service import ChapterService


def test_create_chapter(test_client, chapter_request: CreateChapterRequest):
    response = test_client.post(
        '/chapters', json=chapter_request.model_dump(mode='json')
    )
    json_chapter: ChapterResponse = ChapterResponse.model_validate(
        response.json()
    )

    assert response.status_code == 201
    assert json_chapter.book_id == chapter_request.book_id
    assert json_chapter.id == 3


def test_get_chapter_by_id(
    test_client, chapter_request: CreateChapterRequest, db_session: Session
):
    chapter: Chapter = ChapterService(db_session).create(chapter_request)

    response = test_client.get(f'/chapters/{chapter.id}')
    json_chapter: ChapterResponse = ChapterResponse.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert json_chapter.id == chapter.id
    assert json_chapter == ChapterResponse.model_validate(chapter)


def test_get_chapter_by_note_id(
    test_client,
    instantiate_models_and_populate_db: tuple[
        Book, Chapter, Chapter, Note, Note
    ],
):
    _, c, _, n, _ = instantiate_models_and_populate_db

    response = test_client.get(f'/chapters/by_note/{n.id}')
    json_chapter: ChapterResponse = ChapterResponse.model_validate(
        response.json()
    )
    assert response.status_code == 200
    assert json_chapter == ChapterResponse.model_validate(c)


def test_list_by_book_id(
    test_client,
    instantiate_models_and_populate_db: tuple[
        Book, Chapter, Chapter, Note, Note
    ],
):
    b, c1, c2, _, _ = instantiate_models_and_populate_db

    response = test_client.get(f'/chapters/by_book/{b.id}')

    json_chapters: ChapterResponseList = ChapterResponseList.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert json_chapters.chapters[0] == ChapterResponse.model_validate(c1)
    assert json_chapters.chapters[1] == ChapterResponse.model_validate(c2)


def test_list_all_chapters(
    test_client,
    instantiate_models_and_populate_db: tuple[
        Book, Chapter, Chapter, Note, Note
    ],
):
    _, c1, c2, _, _ = instantiate_models_and_populate_db

    response = test_client.get('/chapters/list/')

    json_chapters: ChapterResponseList = ChapterResponseList.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert json_chapters.chapters[0] == ChapterResponse.model_validate(c1)
    assert json_chapters.chapters[1] == ChapterResponse.model_validate(c2)

