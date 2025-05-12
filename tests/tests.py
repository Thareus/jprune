import unittest
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import JPrune

TEST_JSON_PATH = os.path.join(os.path.dirname(__file__), "test_data.json")

class TestJPrune(unittest.TestCase):
    def setUp(self):
        self.jp = JPrune(TEST_JSON_PATH)
        with open(TEST_JSON_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_get_paths(self):
        paths = self.jp.get_paths(self.data)
        self.assertIn("project.id", paths)
        self.assertIn("project.meta.owner.name", paths)
        self.assertIn("project.data.documents.title", paths)

    def test_show_paths(self):
        result = self.jp.show_paths()
        self.assertIsInstance(result, str)
        self.assertIn("project.id", result)
        self.assertIn("project.meta.owner.name", result)

    def test_show_schema(self):
        schema_str = self.jp.show_schema()
        self.assertIsInstance(schema_str, str)
        schema = json.loads(schema_str)
        self.assertIn("project", schema)
        self.assertIn("data", schema["project"])

    def test_find_key(self):
        keys = self.jp.find_key("id")
        self.assertTrue(any("id" in k for k in keys))
        keys = self.jp.find_key("email")
        self.assertTrue(any("email" in k for k in keys))

    def test_paths_to_structure(self):
        paths = ["a.b.c", "x.y.z"]
        structure = self.jp.paths_to_structure(paths)
        self.assertIn("a", structure)
        self.assertIn("x", structure)
        self.assertIn("b", structure["a"])
        self.assertIn("z", structure["x"]["y"])

    def test_get_value_by_path(self):
        values = self.jp.get_value_by_path(self.data, "project.id")
        self.assertIn("alpha-23984", values)
        values = self.jp.get_value_by_path(self.data, ["project.meta.owner.name", "project.meta.status"])
        self.assertIn("Nelson", values)
        self.assertIn("active", values)

    def test_filter_include(self):
        include_paths = ["project.id", "project.meta.owner.name"]
        result = self.jp.filter(data=self.data, keep_paths=include_paths)
        self.assertIn("alpha-23984", result)
        self.assertIn("Nelson", result)

    def test_filter_exclude(self):
        include_paths = ["project.id", "project.meta.owner.name"]
        exclude_paths = ["project.id"]
        with self.assertRaises(ValueError):
            self.jp.filter(data=self.data, keep_paths=include_paths, exclude_paths=exclude_paths)

    def test_filter_overlap_error(self):
        include_paths = ["project.id"]
        exclude_paths = ["project.id"]
        with self.assertRaises(ValueError):
            self.jp.filter(data=self.data, keep_paths=include_paths, exclude_paths=exclude_paths)

    def test_collapse_to_string(self):
        string = self.jp.collapse_to_string(self.data)
        self.assertIsInstance(string, str)
        self.assertIn("Natural language processing", string)

    def test__remove_nones(self):
        data = {"a": 1, "b": None, "c": {"d": None, "e": 2}, "f": [None, 3]}
        cleaned = self.jp._remove_nones(data)
        self.assertEqual(cleaned, {"a": 1, "c": {"e": 2}, "f": [3]})

    def test__prune_json(self):
        data = {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
        allowed = ["a", "c.d"]
        pruned = self.jp._prune_json(data.copy(), allowed_paths=allowed)
        self.assertEqual(pruned["a"], 1)
        self.assertIsNone(pruned["b"])
        self.assertEqual(pruned["c"]["d"], 3)
        self.assertIsNone(pruned["c"]["e"])

    def test__should_keep(self):
        self.assertTrue(self.jp._should_keep("a", ["a", "a.b"]))
        self.assertTrue(self.jp._should_keep("a", ["a.b"]))
        self.assertFalse(self.jp._should_keep("a", ["b"]))

if __name__ == "__main__":
    unittest.main()
