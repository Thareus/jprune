import json
from typing import Any, Dict, List, Set, Optional, Union

class JPrune:
    def __init__(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.paths = set()

    def get_paths(self, data: Any, current_path: str = "") -> Set[str]:
        """
        Recursively extract all key paths in dot notation.
        Works for dicts and lists.
        """
        paths: Set[str] = set()
        if isinstance(data, dict):
            for k, v in data.items():
                new_path = f"{current_path}.{k}" if current_path else k
                paths.add(new_path)
                paths.update(self.get_paths(v, new_path))
        elif isinstance(data, list):
            for item in data:
                paths.update(self.get_paths(item, current_path))
        return paths

    def show_paths(self) -> str:
        """
        Show all key paths in dot notation.

        :return: string of sorted paths, one per line
        """
        if not self.paths:
            self.paths = self.get_paths(self.data)
        return "\n".join(sorted(self.paths))

    def show_schema(self) -> str:
        """
        Show a schema representation of the JSON structure.

        :return: JSON-formatted string representing the schema
        """
        if not self.paths:
            self.paths = self.get_paths(self.data)
        self.schema = {}
        for key in self.paths:
            parts = key.split('.')
            current = self.schema
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = str(type(part).__name__)
                else:
                    if part not in current or not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
        return json.dumps(self.schema, indent=2)

    def find_key(self, key: str) -> List[str]:
        """
        Find all paths that end with a given key.

        :param key: str, key to search for
        :return: list of matching paths
        """
        if not self.paths:
            self.paths = self.get_paths(self.data)
        matching_keys = []
        for path in self.paths:
            if path.endswith(key):
                matching_keys.append(path)
        return matching_keys

    def paths_to_structure(self, paths: List[str]) -> Dict[str, Any]:
        """
        Convert a list of dot-notated paths into a nested dictionary structure.

        :param paths: list of str, e.g. ["a.b.c", "x.y.z"]
        :return: nested dict with empty dicts as leaf values
        """
        structure = {}
        for path in paths:
            keys = path.split('.')
            current = structure
            for key in keys:
                if key not in current:
                    current[key] = {}
                current = current[key]
        return structure

    def _recurse(self, node: Any, keys: List[str], results: Set[Any]) -> None:
        """
        Recursively traverse a JSON-like structure to collect values at specified paths.

        :param node:    current node in the traversal
        :param keys:    list of keys to follow
        :param results: set to collect matching values
        """
        if not keys:
            # we've consumed the entire path; collect this node
            results.extend([node])
            return

        key, *rest = keys

        if isinstance(node, dict):
            # descend if key exists
            if key in node:
                self._recurse(node[key], rest, results)

        elif isinstance(node, list):
            # try the same full key sequence on each element
            for element in node:
                self._recurse(element, keys, results)

    def get_value_by_path(self, data: Any, paths: Union[str, List[str]]) -> List[Any]:
        """
        Retrieve a set of values from a JSON-like structure by one or more
        dot.notated key paths. If `path` is a list, results from each
        path are unioned into a single set.

        :param data: nested dicts/lists representing JSON
        :param paths: str or list of str, e.g. "a.b.c" or ["a.b", "x.y.z"]
        :return: set of all matching leaf values
        """
        if not data:
            data = self.data
        # normalize to list of strings
        paths = [paths] if isinstance(paths, str) else paths
        results = list()
        for p in paths:
            keys = p.split('.')
            self._recurse(data, keys, results)
        return results

    def _should_keep(self, path: str, allowed_paths: List[str]) -> bool:
        return any(ap == path or ap.startswith(f"{path}.") for ap in allowed_paths)

    def _prune_json(self, obj: Any, path: str = "", allowed_paths: Optional[List[str]] = None) -> Any:
        """
        Recursively prune a JSON object by key paths, removing all other data.

        :param obj: JSON object to prune
        :param path: current path in the traversal (internal use)
        :param allowed_paths: list of paths to keep
        :return: pruned JSON object
        """
        if isinstance(obj, dict):
            keys = list(obj.keys())
            for key in keys:
                full_path = f"{path}.{key}" if path else key
                if self._should_keep(full_path, allowed_paths):
                    obj[key] = self._prune_json(obj[key], full_path, allowed_paths)
                else:
                    obj[key] = None
            return obj
        elif isinstance(obj, list):
            return [self._prune_json(item, path, allowed_paths) for item in obj]
        else:
            return obj

    def _remove_nones(self, obj: Any) -> Optional[Any]:
        """
        Recursively remove all None values from a JSON object.

        :param obj: JSON object to clean
        :return: cleaned JSON object
        """
        if isinstance(obj, dict):
            cleaned = {k: self._remove_nones(v) for k, v in obj.items() if v is not None}
            return cleaned if cleaned else None
        elif isinstance(obj, list):
            cleaned_list = [self._remove_nones(item) for item in obj]
            cleaned_list = [item for item in cleaned_list if item is not None]
            return cleaned_list if cleaned_list else None
        else:
            return obj

    def collapse_to_string(self, data: Any, sep: str = '\n') -> str:
        """
        Traverse any nested dict/list and collect all leaf values into one string.

        :param data: nested dict/list/scalar
        :param sep:  string inserted between values (default: single space)
        :return:     single string of all leaf values
        """
        pieces = []

        def _gather(node: Any) -> None:
            if isinstance(node, str):
                pieces.append(node)
            elif isinstance(node, (int, float, bool)):
                # Convert to string
                pieces.append(str(node))
            elif isinstance(node, dict):
                for v in node.values():
                    _gather(v)
            elif isinstance(node, list):
                for item in node:
                    _gather(item)

        _gather(data)
        return sep.join(pieces)

    def filter(self, data: Optional[Any] = None, keep_paths: Optional[List[str]] = None, exclude_paths: Optional[List[str]] = None) -> str:
        """
        Recursively filter a JSON object by key paths.
        Uses dot notation for keys. List indices are not tracked.
        Includes/excludes all data that matches the given key path structure.
        """
        if not data:
            data = self.data
        if not keep_paths:
            keep_paths = self.paths
        if not exclude_paths:
            exclude_paths = []
        if set(keep_paths).intersection(set(exclude_paths)):
            raise ValueError("Include and exclude paths cannot overlap.")

        keep_paths = list(set([path for path in keep_paths if path not in exclude_paths]))
        pruned_json = self._prune_json(data, allowed_paths=keep_paths)
        cleaned_json = self._remove_nones(pruned_json)
        return cleaned_json
    
    def extract_text(self, data, paths):
        result = self.filter(data, keep_paths=paths)
        return self.collapse_to_string(result)