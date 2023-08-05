import unittest
import os
import warnings
from fetching import Fetching


class TestFetch(unittest.TestCase):
    f = Fetching()
    fixtures_dir = f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/"

    def test_workflow_single_repo(self):

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        targets = [
            {
                "name": "nthparty/fetch",
                "files": ["fetching/fetching.py"],
                "ref": "055ad6af491f5cd7d308f4fbc5c32852d8748f59"
            }
        ]

        dependencies = self.f.fetch(targets)
        content = self.f.build(dependencies)
        self.assertTrue(content == open(f"{self.fixtures_dir}/fetch_single_repo.txt").read())

    def test_workflow_multiple_repo(self):

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        targets = [
            {
                "name": "nthparty/fetching",
                "files": ["fetching/fetching.py"],
                "ref": "055ad6af491f5cd7d308f4fbc5c32852d8748f59"
            },
            {
                "name": "nthparty/oblivious",
                "files": ["oblivious/oblivious.py", "test/test_oblivious.py"],
                "ref": "daa92da7197cdcd5dfc89854fa1b672f37096e74"
            }
        ]

        dependencies = self.f.fetch(targets)
        content = self.f.build(dependencies)
        self.assertTrue(content == open(f"{self.fixtures_dir}/fetch_multiple_repo.txt").read())
