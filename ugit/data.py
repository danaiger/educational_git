import hashlib
import json
import os
import shutil

from collections import namedtuple
from contextlib import contextmanager


# Will be initialized in cli.main()
GIT_DIR = None


@contextmanager
def change_git_dir(new_dir):
    global GIT_DIR
    old_dir = GIT_DIR
    GIT_DIR = f"{new_dir}/.ugit"
    yield
    GIT_DIR = old_dir


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f"{GIT_DIR}/objects")


RefValue = namedtuple("RefValue", ["symbolic", "value"])


def update_ref(ref_name: str, value: RefValue, deref: bool = True) -> None:
    target_ref = _get_ref_internal(ref_name, deref)[0]

    assert value.value
    if value.symbolic:
        content = f"ref: {value.value}"
    else:
        content = value.value

    ref_path = f"{GIT_DIR}/{target_ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w") as f:
        f.write(content)


def get_ref(ref_name: str, deref: bool = True) -> RefValue:
    return _get_ref_internal(ref_name, deref)[1]


def delete_ref(ref_name: str, deref: bool = True) -> None:
    target_ref = _get_ref_internal(ref_name, deref)[0]
    os.remove(f"{GIT_DIR}/{target_ref}")


def _get_ref_internal(ref_name: str, deref: bool) -> tuple[str, RefValue]:
    ref_path = f"{GIT_DIR}/{ref_name}"
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()

    symbolic = bool(value) and value.startswith("ref:")
    if symbolic:
        symbolic_target = value.split(":", 1)[1].strip()
        if deref:
            return _get_ref_internal(symbolic_target, deref=True)
        value = symbolic_target

    return ref_name, RefValue(symbolic=symbolic, value=value)


def iter_refs(prefix: str = "", deref: bool = True):
    ref_names = ["HEAD", "MERGE_HEAD"]
    for root, _, filenames in os.walk(f"{GIT_DIR}/refs/"):
        root = os.path.relpath(root, GIT_DIR)
        ref_names.extend(f"{root}/{name}" for name in filenames)

    for ref_name in ref_names:
        if not ref_name.startswith(prefix):
            continue
        ref_value = get_ref(ref_name, deref=deref)
        if ref_value.value:
            yield ref_name, ref_value


@contextmanager
def get_index():
    index = {}
    if os.path.isfile(f"{GIT_DIR}/index"):
        with open(f"{GIT_DIR}/index") as f:
            index = json.load(f)

    yield index

    with open(f"{GIT_DIR}/index", "w") as f:
        json.dump(index, f)


def hash_object(data, type_="blob"):
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(obj)
    return oid


def get_object(oid, expected="blob"):
    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f"Expected {expected}, got {type_}"
    return content


def object_exists(oid):
    return os.path.isfile(f"{GIT_DIR}/objects/{oid}")


def fetch_object_if_missing(oid, remote_git_dir):
    if object_exists(oid):
        return
    remote_git_dir += "/.ugit"
    shutil.copy(f"{remote_git_dir}/objects/{oid}", f"{GIT_DIR}/objects/{oid}")


def push_object(oid, remote_git_dir):
    remote_git_dir += "/.ugit"
    shutil.copy(f"{GIT_DIR}/objects/{oid}", f"{remote_git_dir}/objects/{oid}")
