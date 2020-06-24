import unittest

import pandas as pd

from gharchive.models import Archive, ArchiveElement
from tests.config import DATA_FILE


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


class TestFilterModels(TestCreateModels):
    def test_single_filter(self):
        compare_str = "WatchEvent"
        archive = self.archive.filter([("type", compare_str)])
        for elem in archive.data:
            assert elem.type == compare_str
        assert len(archive.data) > 0

    def test_nested_filter(self):
        compare_str = "https://api.github.com/users/soumith"
        archive = self.archive.filter([("actor.url", compare_str)])
        for elem in archive.data:
            assert elem.actor.url == compare_str
        assert len(archive.data) > 0

    def test_dual_filter(self):
        compare_str_1 = "https://api.github.com/users/jamezb"
        compare_str_2 = "WatchEvent"
        archive = self.archive.filter(
            [("actor.url", compare_str_1), ("type", compare_str_2)]
        )
        for elem in archive.data:
            assert elem.actor.url == compare_str_1
            assert elem.type == compare_str_2
        assert len(archive.data) > 0


class TestSerializeModels(TestCreateModels):
    def test_to_df(self):
        df = self.archive.to_df()

        assert len(df) == 7427
        assert len(df.columns) == 141

        first_row = df.iloc[0]
        assert first_row["id"] == "2489395767"
        assert first_row["type"] == "PushEvent"
        assert pd.isnull(first_row["payload_commits_author_email_20"])

        last_row = df.iloc[-1]
        assert last_row["id"] == "2489418153"
        assert last_row["type"] == "PushEvent"
        assert pd.isnull(last_row["payload_commits_author_email_20"])
