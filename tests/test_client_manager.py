
from revision.client import Client
from revision.client_manager import ClientManager
from revision.config import Config
from revision.mixins import DotDictMixin

dummy_client = {
    "key": "dummy",
    "module": "revision.test.DummyClient",
    "local_path": "./tests/data",
    "remote_path": "",
    "revision_file": "CHANGELOG.md"
}

config = Config({
    "clients": [ dummy_client ]
})

def test_client_manager_prepare():
    manager = ClientManager(config.clients)

    assert len(manager) == 1
    assert "dummy" in manager
    assert isinstance(manager["dummy"], Client)

    client = manager.get_client("dummy")
    client.state.clear()

def test_client_manager_instantiate_client():
    manager = ClientManager()
    client = manager.instantiate_client(DotDictMixin(dummy_client))

    assert isinstance(client, Client)
    assert client.key == "dummy"

    client.state.clear()

def test_client_manager_has_client():
    manager = ClientManager(config.clients)

    assert manager.has_client("dummy") is True
    assert manager.has_client("failed_key") is False

    client = manager.get_client("dummy")
    client.state.clear()

def test_client_manager_get_client():
    manager = ClientManager(config.clients)

    client = manager.get_client("dummy")

    assert isinstance(client, Client)
    assert client.name == "Dummy storage for testing"
    assert client.key == "dummy"
    assert client.client_key == "test"

    client.state.clear()

    client = manager.get_client("failed_key")

    assert client is None

def test_client_manager_add_client():
    manager = ClientManager()

    client = manager.instantiate_client(DotDictMixin(dummy_client))

    manager.add_client(client)

    assert len(manager) == 1
    assert "dummy" in manager

    client = manager.get_client("dummy")

    assert isinstance(client, Client)
    assert client.name == "Dummy storage for testing"
    assert client.key == "dummy"
    assert client.client_key == "test"

    client.state.clear()
