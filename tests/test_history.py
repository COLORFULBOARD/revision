
import os

from revision.data import Revision
from revision.history import History

def test_history_init():
    history = History()
    history.clear()

    assert isinstance(history.revisions, list)
    assert len(history.revisions) == 0
    assert isinstance(history.current_index, int)
    assert history.current_index == 0

def test_history_load():
    history = History()
    history.clear()

    revision_file_path = os.path.join(
        os.path.dirname(__file__),
        'test_history_changelog.md'
    )

    history.load(revision_file_path)

    assert isinstance(history.revisions, list)
    assert len(history.revisions) == 2
    assert isinstance(history.current_index, int)
    assert history.current_index == 0
    assert history.current_revision.description == "test description 1"

def test_history_clear():
    history = History()
    history.clear()

    revision_file_path = os.path.join(
        os.path.dirname(__file__),
        'test_history_changelog.md'
    )

    history.load(revision_file_path)

    assert isinstance(history.revisions, list)
    assert len(history.revisions) == 2
    assert history.current_index == 0

    history.clear()

    assert isinstance(history.revisions, list)
    assert len(history.revisions) == 0
    assert history.current_index == 0

def test_history_checkout():
    history = History()
    history.clear()

    revision_file_path = os.path.join(
        os.path.dirname(__file__),
        'test_history_changelog.md'
    )

    history.load(revision_file_path)

    assert isinstance(history.revisions, list)
    assert len(history.revisions) == 2
    assert history.current_index == 0

    revision_id = history.revisions[1].revision_id

    history.checkout(revision_id)

    assert history.current_index == 1

def test_history_prepend_and_insert():
    history = History()
    history.clear()

    revision1 = Revision.create(
        description="description1",
        message="message1"
    )
    revision2 = Revision.create(
        description="description2",
        message="message2"
    )
    revision3 = Revision.create(
        description="description3",
        message="message3"
    )

    assert len(history.revisions) == 0

    history.prepend(revision1)

    assert len(history.revisions) == 1
    assert history.revisions[0].description == "description1"
    assert history.current_index == 0
    assert history.current_revision.description == "description1"

    history.prepend(revision2)

    assert len(history.revisions) == 2
    assert history.revisions[0].description == "description2"
    assert history.revisions[1].description == "description1"
    assert history.current_index == 0
    assert history.current_revision.description == "description2"

    history.insert(revision3, 1)

    assert len(history.revisions) == 3
    assert history.revisions[0].description == "description2"
    assert history.revisions[1].description == "description3"
    assert history.revisions[2].description == "description1"
    assert history.current_index == 0
    assert history.current_revision.description == "description2"
