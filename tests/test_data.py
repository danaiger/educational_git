from ugit import data


def test_init_creates_repository(temp_dir):
    """init() creates .ugit directory"""
    data.init()

    assert (temp_dir / ".ugit").is_dir()


def test_hash_object_returns_consistent_oid(ugit_repo):
    """Same content always produces same OID"""
    content = b"hello world"

    oid1 = data.hash_object(content)
    oid2 = data.hash_object(content)

    assert oid1 == oid2


def test_hash_object_different_content_different_oid(ugit_repo):
    """Different content produces different OIDs"""
    oid1 = data.hash_object(b"content one")
    oid2 = data.hash_object(b"content two")

    assert oid1 != oid2


def test_get_object_retrieves_stored_content(ugit_repo):
    """Can retrieve exactly what was stored"""
    original_content = b"test content here"
    oid = data.hash_object(original_content)

    retrieved = data.get_object(oid)

    assert retrieved == original_content


def test_hash_and_get_with_type(ugit_repo):
    """Can store and retrieve objects with different types"""
    content = b"some data"

    tree_oid = data.hash_object(content, type_="tree")
    commit_oid = data.hash_object(content, type_="commit")

    assert data.get_object(tree_oid, expected="tree") == content
    assert data.get_object(commit_oid, expected="commit") == content


def test_index_persistence(ugit_repo):
    """Index changes persist across get_index() calls"""
    with data.get_index() as index:
        index["file.txt"] = "abc123"

    with data.get_index() as index:
        assert index["file.txt"] == "abc123"
