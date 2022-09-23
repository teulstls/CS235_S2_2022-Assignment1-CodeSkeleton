from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User('jakm', '123456789')
    in_memory_repo.add_user(user)

    user = in_memory_repo.get_user('jakm')
    assert user == User('jakm', '123456789')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('asdfasdfa')
    assert user is None


def test_repository_can_retrieve_article_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_tracks()

    # Check that the query returned 6 Articles.
    assert number_of_articles == 1855


def test_repository_can_add_article(in_memory_repo):
    article = Track(
        2020,
        'test'
    )
    in_memory_repo.add_track(article)

    assert in_memory_repo.get_track(2020) is article


def test_repository_can_retrieve_article(in_memory_repo):
    abc = Track(
        2021,
        'testtest'
    )
    in_memory_repo.add_track(abc)
    article = in_memory_repo.get_last_track()

    # Check that the Article has the expected title.
    assert article.title == 'testtest'


def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    article = in_memory_repo.get_track(9999)
    assert article is None


def test_repository_can_retrieve_articles_by_date(in_memory_repo):
    articles = in_memory_repo.get_tracks_by_name("Abominog")

    # Check that the query returned 3 Articles.
    assert len(articles) == 2


def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(in_memory_repo):
    articles = in_memory_repo.get_tracks_by_name("asdfasdfasdf")
    assert len(articles) == 0


def test_repository_can_retrieve_tags(in_memory_repo):
    tags: List[Genre] = in_memory_repo.get_genres()

    assert len(tags) == 55


def test_repository_can_get_first_article(in_memory_repo):
    article = in_memory_repo.get_first_track()
    assert article.title == "Father's Day"


def test_repository_can_get_last_article(in_memory_repo):
    article = in_memory_repo.get_last_track()
    assert article.title == '4'


def test_repository_can_get_articles_by_ids(in_memory_repo):
    articles = in_memory_repo.get_tracks_by_id([1, 2, 3])

    assert len(articles) == 3
    assert articles[
               0].title == "Father's Day"
    assert articles[1].title == "Peel Back The Mountain Sky"
    assert articles[2].title == 'Ed De Goem'


def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_tracks_by_id([1, 8888])

    assert len(articles) == 1
    assert articles[
               0].title == "Father's Day"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_tracks_by_id([0, 8463])

    assert len(articles) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    article_ids = in_memory_repo.get_track_ids_for_genre('Blues')
    gen = list()
    for id in article_ids:
        track = in_memory_repo.get_track(id)
        for genre in track.genres:
            gen.append(genre.name)
    assert 'Blues' in gen


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    article_ids = in_memory_repo.get_track_ids_for_genre('abcdefg')

    assert len(article_ids) == 0


def test_repository_returns_date_of_previous_article(in_memory_repo):
    article = in_memory_repo.get_track(2)
    previous_date = in_memory_repo.get_name_of_previous_track(article)

    assert previous_date == 'Abominog'


def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
    article = in_memory_repo.get_track(1)
    previous_date = in_memory_repo.get_name_of_previous_track(article)

    assert previous_date is None


def test_repository_returns_date_of_next_article(in_memory_repo):
    article = in_memory_repo.get_track(1)
    next_date = in_memory_repo.get_name_of_next_track(article)

    assert next_date == 'Adept'


def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
    article = in_memory_repo.get_last_track()
    next_date = in_memory_repo.get_name_of_next_track(article)

    assert next_date is None


def test_repository_can_add_a_tag(in_memory_repo):
    tag = Genre(999, 'Motoring')
    in_memory_repo.add_genre(tag)

    assert tag in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_track(2)
    comment = Review(user, article, "Trump's onto it!", 5)

    in_memory_repo.add_review(comment)

    assert comment in in_memory_repo.get_reviews()


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 0



