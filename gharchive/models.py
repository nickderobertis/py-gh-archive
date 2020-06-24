import json
from typing import (
    Optional,
    Any,
    List,
    TypeVar,
    Type,
    cast,
    Callable,
    Sequence,
    Tuple,
    Union,
)
from datetime import datetime
import dateutil.parser
import requests

from gharchive.unzip import decompress

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


# TODO [#1]: support Timeline API format
#
# Any records from 2/12/2011-12/31/2014 were from the deprecated Timeline API
# and so come in a different format. Need to parse them into the same models.
# Currently the code will fail to parse any responses from this time period.
# There is already a 2012-06-14-15.json.gz in the test data which triggers this.
# Also update gharchive.search.SUPPORTED_BEGIN_YEAR after this and add constraints
# for not being earlier in 2011.


class Actor:
    id: Optional[int]
    login: Optional[str]
    display_login: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    avatar_url: Optional[str]

    def __init__(
        self,
        id: Optional[int],
        login: Optional[str],
        display_login: Optional[str],
        gravatar_id: Optional[str],
        url: Optional[str],
        avatar_url: Optional[str],
    ) -> None:
        self.id = id
        self.login = login
        self.display_login = display_login
        self.gravatar_id = gravatar_id
        self.url = url
        self.avatar_url = avatar_url

    @staticmethod
    def from_dict(obj: Any) -> "Actor":
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        login = from_union([from_str, from_none], obj.get("login"))
        display_login = from_union([from_str, from_none], obj.get("display_login"))
        gravatar_id = from_union([from_str, from_none], obj.get("gravatar_id"))
        url = from_union([from_str, from_none], obj.get("url"))
        avatar_url = from_union([from_str, from_none], obj.get("avatar_url"))
        return Actor(id, login, display_login, gravatar_id, url, avatar_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["login"] = from_union([from_str, from_none], self.login)
        result["display_login"] = from_union([from_str, from_none], self.display_login)
        result["gravatar_id"] = from_union([from_str, from_none], self.gravatar_id)
        result["url"] = from_union([from_str, from_none], self.url)
        result["avatar_url"] = from_union([from_str, from_none], self.avatar_url)
        return result


class Author:
    name: Optional[str]
    email: Optional[str]

    def __init__(self, name: Optional[str], email: Optional[str]) -> None:
        self.name = name
        self.email = email

    @staticmethod
    def from_dict(obj: Any) -> "Author":
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        email = from_union([from_str, from_none], obj.get("email"))
        return Author(name, email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["email"] = from_union([from_str, from_none], self.email)
        return result


class Commit:
    sha: Optional[str]
    author: Optional[Author]
    message: Optional[str]
    distinct: Optional[bool]
    url: Optional[str]

    def __init__(
        self,
        sha: Optional[str],
        author: Optional[Author],
        message: Optional[str],
        distinct: Optional[bool],
        url: Optional[str],
    ) -> None:
        self.sha = sha
        self.author = author
        self.message = message
        self.distinct = distinct
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> "Commit":
        assert isinstance(obj, dict)
        sha = from_union([from_str, from_none], obj.get("sha"))
        author = from_union([Author.from_dict, from_none], obj.get("author"))
        message = from_union([from_str, from_none], obj.get("message"))
        distinct = from_union([from_bool, from_none], obj.get("distinct"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Commit(sha, author, message, distinct, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sha"] = from_union([from_str, from_none], self.sha)
        result["author"] = from_union(
            [lambda x: to_class(Author, x), from_none], self.author
        )
        result["message"] = from_union([from_str, from_none], self.message)
        result["distinct"] = from_union([from_bool, from_none], self.distinct)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class Payload:
    ref: Optional[str]
    ref_type: Optional[str]
    pusher_type: Optional[str]
    push_id: Optional[int]
    size: Optional[int]
    distinct_size: Optional[int]
    head: Optional[str]
    before: Optional[str]
    commits: Optional[List[Commit]]

    def __init__(
        self,
        ref: Optional[str],
        ref_type: Optional[str],
        pusher_type: Optional[str],
        push_id: Optional[int],
        size: Optional[int],
        distinct_size: Optional[int],
        head: Optional[str],
        before: Optional[str],
        commits: Optional[List[Commit]],
    ) -> None:
        self.ref = ref
        self.ref_type = ref_type
        self.pusher_type = pusher_type
        self.push_id = push_id
        self.size = size
        self.distinct_size = distinct_size
        self.head = head
        self.before = before
        self.commits = commits

    @staticmethod
    def from_dict(obj: Any) -> "Payload":
        assert isinstance(obj, dict)
        ref = from_union([from_str, from_none], obj.get("ref"))
        ref_type = from_union([from_str, from_none], obj.get("ref_type"))
        pusher_type = from_union([from_str, from_none], obj.get("pusher_type"))
        push_id = from_union([from_int, from_none], obj.get("push_id"))
        size = from_union([from_int, from_none], obj.get("size"))
        distinct_size = from_union([from_int, from_none], obj.get("distinct_size"))
        head = from_union([from_str, from_none], obj.get("head"))
        before = from_union([from_str, from_none], obj.get("before"))
        commits = from_union(
            [lambda x: from_list(Commit.from_dict, x), from_none], obj.get("commits")
        )
        return Payload(
            ref,
            ref_type,
            pusher_type,
            push_id,
            size,
            distinct_size,
            head,
            before,
            commits,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["ref"] = from_union([from_str, from_none], self.ref)
        result["ref_type"] = from_union([from_str, from_none], self.ref_type)
        result["pusher_type"] = from_union([from_str, from_none], self.pusher_type)
        result["push_id"] = from_union([from_int, from_none], self.push_id)
        result["size"] = from_union([from_int, from_none], self.size)
        result["distinct_size"] = from_union([from_int, from_none], self.distinct_size)
        result["head"] = from_union([from_str, from_none], self.head)
        result["before"] = from_union([from_str, from_none], self.before)
        result["commits"] = from_union(
            [lambda x: from_list(lambda x: to_class(Commit, x), x), from_none],
            self.commits,
        )
        return result


class Repo:
    id: Optional[int]
    name: Optional[str]
    url: Optional[str]

    def __init__(
        self, id: Optional[int], name: Optional[str], url: Optional[str]
    ) -> None:
        self.id = id
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> "Repo":
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Repo(id, name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class ArchiveElement:
    id: Optional[str]
    type: Optional[str]
    actor: Optional[Actor]
    repo: Optional[Repo]
    payload: Optional[Payload]
    public: Optional[bool]
    created_at: Optional[datetime]

    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        actor: Optional[Actor],
        repo: Optional[Repo],
        payload: Optional[Payload],
        public: Optional[bool],
        created_at: Optional[datetime],
    ) -> None:
        self.id = id
        self.type = type
        self.actor = actor
        self.repo = repo
        self.payload = payload
        self.public = public
        self.created_at = created_at

    @staticmethod
    def from_dict(obj: Any) -> "ArchiveElement":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        type = from_union([from_str, from_none], obj.get("type"))
        actor = from_union([Actor.from_dict, from_none], obj.get("actor"))
        repo = from_union([Repo.from_dict, from_none], obj.get("repo"))
        payload = from_union([Payload.from_dict, from_none], obj.get("payload"))
        public = from_union([from_bool, from_none], obj.get("public"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        return ArchiveElement(id, type, actor, repo, payload, public, created_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["type"] = from_union([from_str, from_none], self.type)
        result["actor"] = from_union(
            [lambda x: to_class(Actor, x), from_none], self.actor
        )
        result["repo"] = from_union([lambda x: to_class(Repo, x), from_none], self.repo)
        result["payload"] = from_union(
            [lambda x: to_class(Payload, x), from_none], self.payload
        )
        result["public"] = from_union([from_bool, from_none], self.public)
        result["created_at"] = from_union(
            [lambda x: x.isoformat(), from_none], self.created_at
        )
        return result


class Archive:
    data: List[ArchiveElement]

    def __init__(self, data: List[ArchiveElement]):
        self.data = data

    @classmethod
    def from_dict_list(cls, data: List[dict]):
        archive_elems = [ArchiveElement.from_dict(d) for d in data]
        return cls(archive_elems)

    @classmethod
    def from_response(cls, resp: requests.Response):
        return cls.from_gzip_bytes(resp.content)

    @classmethod
    def from_gzip_bytes(cls, b: bytes):
        data_str = decompress(b).decode("utf8")
        data_strs = [s for s in data_str.split("\n") if s]
        del data_str
        json_str = "[" + ", ".join(data_strs) + "]"
        del data_strs
        data = json.loads(json_str)
        return cls.from_dict_list(data)

    def to_dict_list(self) -> List[dict]:
        return [elem.to_dict() for elem in self.data]

    def __add__(self, other):
        cls = self.__class__
        return cls(self.data + other.data)

    def filter(
        self, filters: Sequence[Tuple[str, Union[int, float, str]]]
    ) -> "Archive":
        new_elems = []
        for elem in self.data:
            valid = True
            for (attr, value) in filters:
                getattr_list = attr.split(".")
                filter_value = elem
                for gattr in getattr_list:
                    filter_value = getattr(filter_value, gattr)
                if filter_value != value:
                    valid = False
                    break
            if valid:
                new_elems.append(elem)
        cls = self.__class__
        return cls(new_elems)
