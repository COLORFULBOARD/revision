
from revision.client import Client
from revision.client_manager import ClientManager
from revision.config import Config
from revision.mixins import DotDictMixin

config = Config({
    "clients": [
        {
            "key": "dataset",
            "module": "revision.test.DummyClient",
            "dir_path": "./tests/data",
            "revision_file": "CHANGELOG.md"
        }
    ]
})

def test_client_manager_prepare():
    manager = ClientManager()
    manager.prepare(config.clients)

    assert len(manager.items) == 1
    assert "dataset" in manager.items
    assert isinstance(manager.items['dataset'], Client)

def test_client_manager_instantiate_client():
    manager = ClientManager()
    client = manager.instantiate_client(DotDictMixin({
        "key": "dataset",
        "module": "revision.test.DummyClient",
        "dir_path": "./tests/data",
        "revision_file": "CHANGELOG.md"
    }))

    assert isinstance(client, Client)
    assert client.name == "Dummy storage for testing"
    assert client.key == "dataset"
    assert client.client_key == "test"

def test_client_manager_has_client():
    manager = ClientManager()
    manager.prepare(config.clients)

    assert manager.has_client("dataset")

    assert manager.has_client("failed_key") is False

def test_client_manager_get_client():
    manager = ClientManager()
    manager.prepare(config.clients)

    client = manager.get_client("dataset")

    assert isinstance(client, Client)
    assert client.name == "Dummy storage for testing"
    assert client.key == "dataset"
    assert client.client_key == "test"

    client = manager.get_client("failed_key")

    assert client is None

def test_client_manager_get_client():
    manager = ClientManager()

    client = manager.instantiate_client(DotDictMixin({
        "key": "dataset",
        "module": "revision.test.DummyClient",
        "dir_path": "./tests/data",
        "revision_file": "CHANGELOG.md"
    }))

    manager.add_client(client)

    assert len(manager.items) == 1
    assert "dataset" in manager.items

    client = manager.get_client("dataset")

    assert isinstance(client, Client)
    assert client.name == "Dummy storage for testing"
    assert client.key == "dataset"
    assert client.client_key == "test"
