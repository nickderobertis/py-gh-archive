import unittest
import os

from gharchive.models import Archive, ArchiveElement

DATA_DIR = os.path.join("tests", "data")
DATA_FILE = os.path.join(DATA_DIR, "2015-01-01-1.json.gz")


class TestCreateModels(unittest.TestCase):
    archive: Archive
    elem: ArchiveElement

    def setUp(self) -> None:
        with open(DATA_FILE, "rb") as f:
            self.archive = Archive.from_gzip_bytes(f.read())
            self.elem = self.archive.data[0]

    def test_create(self):
        assert self.elem.to_dict() == {
            "id": "2489395767",
            "type": "PushEvent",
            "actor": {
                "id": 1310570,
                "login": "soumith",
                "display_login": None,
                "gravatar_id": "",
                "url": "https://api.github.com/users/soumith",
                "avatar_url": "https://avatars.githubusercontent.com/u/1310570?",
            },
            "repo": {
                "id": 28067809,
                "name": "soumith/fbcunn",
                "url": "https://api.github.com/repos/soumith/fbcunn",
            },
            "payload": {
                "ref": "refs/heads/master",
                "ref_type": None,
                "pusher_type": None,
                "push_id": 536752122,
                "size": 4,
                "distinct_size": 4,
                "head": "fa6048ec9b9eeafd12cee5f81324f355e1f2a198",
                "before": "2d06657267b32e0c8e193c617039da200f710195",
                "commits": [
                    {
                        "sha": "dbd68d30ee1f7b60d404553fc1c6226ebb374c8e",
                        "author": {
                            "name": "Soumith Chintala",
                            "email": "88de463b5797707cf3425f85a415c3d869db732b@gmail.com",
                        },
                        "message": "back to old structure, except lua files moved out",
                        "distinct": True,
                        "url": "https://api.github.com/repos/soumith/fbcunn/commits/dbd68d30ee1f7b60d404553fc1c6226ebb374c8e",
                    },
                    {
                        "sha": "5567f9f5a83d7fe3320b18e5b89405e8a5ca77e6",
                        "author": {
                            "name": "Soumith Chintala",
                            "email": "88de463b5797707cf3425f85a415c3d869db732b@gmail.com",
                        },
                        "message": "...",
                        "distinct": True,
                        "url": "https://api.github.com/repos/soumith/fbcunn/commits/5567f9f5a83d7fe3320b18e5b89405e8a5ca77e6",
                    },
                    {
                        "sha": "58a83b277328eca811d3a37cf171b2fc4fcd87af",
                        "author": {
                            "name": "Soumith Chintala",
                            "email": "88de463b5797707cf3425f85a415c3d869db732b@gmail.com",
                        },
                        "message": "...",
                        "distinct": True,
                        "url": "https://api.github.com/repos/soumith/fbcunn/commits/58a83b277328eca811d3a37cf171b2fc4fcd87af",
                    },
                    {
                        "sha": "fa6048ec9b9eeafd12cee5f81324f355e1f2a198",
                        "author": {
                            "name": "Soumith Chintala",
                            "email": "88de463b5797707cf3425f85a415c3d869db732b@gmail.com",
                        },
                        "message": "...",
                        "distinct": True,
                        "url": "https://api.github.com/repos/soumith/fbcunn/commits/fa6048ec9b9eeafd12cee5f81324f355e1f2a198",
                    },
                ],
            },
            "public": True,
            "created_at": "2015-01-01T01:00:00+00:00",
        }
