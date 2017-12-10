
import os
import shutil

from revision.config import Config, read_config


def test_read_config():

    #: pass path string

    test_revision_path = os.path.join(
        os.path.dirname(__file__),
        '.revision/config.json'
    )

    config = read_config(test_revision_path)

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    #: pass dict object

    config = read_config({
        "clients": [
            {
                "key": "dataset",
                "module": "revision.client.DummyClient",
                "local_path": "./tests/data",
                "remote_path": ""
            }
        ]
    })

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    #: pass nothing

    rev_dirpath = os.path.normpath(os.path.join(
        os.path.dirname(__file__),
        '../.revision'
    ))
    if not os.path.isdir(rev_dirpath):
        os.mkdir(rev_dirpath)
    revision_path = os.path.join(
        rev_dirpath,
        'config.json'
    )

    shutil.copy2(test_revision_path, revision_path)

    config = read_config()

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    shutil.rmtree(rev_dirpath)
