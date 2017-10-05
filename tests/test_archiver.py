
import os
import shutil

from revision.archiver import Archiver

def test_has_path():
    archiver = Archiver()

    assert archiver.has_path is False

    archiver = Archiver(
        target_path="/path/to/source",
        zip_path="/path/to/zipfile"
    )

    assert archiver.has_path is True
    assert archiver.target_path == "/path/to/source"
    assert archiver.zip_path == "/path/to/zipfile"

def test_archive():
    archiver = Archiver()

    try:
        archiver.archive()
        assert False
    except RuntimeError:
        pass

    dir_path = os.path.join(
        os.path.dirname(__file__),
        'data/imgs'
    )
    zip_path = os.path.join(
        os.path.dirname(__file__),
        'tmp/test_archive.zip'
    )

    if os.path.exists(zip_path):
        os.remove(zip_path)

    archiver = Archiver(
        target_path=dir_path,
        zip_path=zip_path
    )

    archiver.archive()

    assert os.path.exists(zip_path)

def test_unarchive():
    archiver = Archiver()

    try:
        archiver.unarchive()
        assert False
    except RuntimeError:
        pass

    dest_path = os.path.join(
        os.path.dirname(__file__),
        'tmp/test_archive'
    )
    zip_path = os.path.join(
        os.path.dirname(__file__),
        'tmp/test_archive.zip'
    )

    if os.path.isdir(dest_path):
        shutil.rmtree(dest_path, ignore_errors=True)

    archiver = Archiver(
        target_path=dest_path,
        zip_path=zip_path
    )

    archiver.unarchive()

    assert os.path.isdir(dest_path)
    assert len(os.listdir(dest_path)) == 2
