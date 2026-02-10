from datetime import datetime


def test_book_instatiation_sets_necessary_fields(
    instantiate_models_and_populate_db,
):
    book, _, _, _, _ = instantiate_models_and_populate_db

    assert book.title == 'Test Book'
    assert book.author == 'Test Author'
    assert book.edition == 1
    assert book.release_date == datetime(2026, 6, 2)
    assert book.publisher == 'Test Publisher'
    assert book.isbn_10 == '0-321-12742-0'
    assert book.isbn_13 == '978-0-321-12742-6'
    assert book.cover_img_url == 'test-cover.jpg'


def test_chapter_instatiation_sets_necessary_fields(
    instantiate_models_and_populate_db,
):
    _, chapter, _, _, _ = instantiate_models_and_populate_db
    assert chapter.title == 'Test Chapter 1'


def test_note_instatiation_sets_necessary_fields(
    instantiate_models_and_populate_db,
):
    _, _, _, note, _ = instantiate_models_and_populate_db
    assert note.title == 'Test Note 1'
    assert note.content == 'Test Note 1 Content'
