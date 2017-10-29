
import os
import shutil

from revision.config import Config, read_config


def test_read_config():

    #: pass path string

    test_revision_path = os.path.join(
        os.path.dirname(__file__),
        'test_revision.json'
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
                "remote_path": "",
                "revision_file": "CHANGELOG.md"
            }
        ]
    })

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    #: pass nothing

    revision_path = os.path.join(
        os.path.dirname(__file__),
        '../.revision.json'
    )

    shutil.copy2(test_revision_path, revision_path)

    config = read_config()

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    os.remove(revision_path)
