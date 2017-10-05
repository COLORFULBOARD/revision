
import os
import shutil

from revision.config import Config, get_config


def test_get_config():
    test_revision_path = os.path.join(
        os.path.dirname(__file__),
        'test_revision.json'
    )

    config = get_config(os.getcwd(), test_revision_path)

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    config = get_config(os.getcwd(), {
        "clients": [
            {
                "key": "dataset",
                "module": "revision.client.DummyClient",
                "dir_path": "./tests/data",
                "revision_file": "CHANGELOG.md"
            }
        ]
    })

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    revision_path = os.path.join(
        os.path.dirname(__file__),
        '../.revision.json'
    )

    shutil.copy2(test_revision_path, revision_path)

    config = get_config(os.getcwd())

    assert isinstance(config, Config)
    assert config.clients[0].key == "dataset"

    os.remove(revision_path)
