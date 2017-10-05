
from revision.util import make_hash_id

def test_make_hash_id():
    hash_id = make_hash_id()

    assert len(hash_id) is 40
    assert type(hash_id) is str
