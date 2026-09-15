"""Rippling Q003 + LC 588 — In-Memory File System

Description
-----------
Implement an in-memory file system with directories and text files. Support
listing, nested directory creation, file creation/appending, and reading.
Extend it with deleting files/directories and searching a directory subtree.
No real files on the computer are created or deleted.

Stage 1 — LC 588 interface
    ls(path) -> list[str]
        Directory: sorted immediate child names (files and directories).
        File: a list containing only its filename, not its full path.
    mkdir(path) -> None
        Create missing directories along the path. Existing directories remain.
    addContentToFile(filePath, content) -> None
        Create the file if absent; otherwise APPEND content. Parent exists.
    readContentFromFile(filePath) -> str
        Return the complete file content.

LC 588 constraints verified using the logged-in Premium session (2026-09-15):
    Valid inputs; file parent exists; lowercase names; path length 1..100;
    content length 1..50; at most 300 calls; mkdir target does not exist.
    Empty files, repeated mkdir and 1500-level paths below are local extensions.

Stage 2 — Rippling deletion extension
    delete(path) -> None
        Remove a file or an entire directory subtree. The target exists and
        is not root. Recursive deletion is a LOCAL PRACTICE assumption.

Stage 3 — Rippling search/deep nesting extension
    search(name, directory="/") -> list[str]
        Find files AND directories with exactly this basename among all
        descendants of directory. Return sorted absolute paths.
        Do not include the starting directory itself. No matches returns [].
        Exact-name matching, subtree scope and output format are LOCAL choices;
        existing reports say efficient search without specifying its contract.

Input assumptions — confirm verbally, do not validate in code
------------------------------------------------------------
- Inputs have the stated types. Paths are absolute and canonical: /a/b, no
  repeated slashes, trailing slash (except /), '.' or '..'. Names are nonempty.
- Names are case-sensitive. No file/directory name conflicts within a directory.
- Intermediate path components are directories. Read, list, delete and search
  targets exist; search starts at a directory. The file parent exists on write.
- mkdir may create missing ancestors. Calling mkdir on an existing directory
  is allowed. An empty file is allowed in this local exercise.
- Paths can be deeply nested: use iterative traversal rather than recursion.
- No permissions, symlinks, persistence, current working directory or concurrency.

Example 1 — LC 588 operation sequence
Input:
    fs = FileSystem()
    fs.ls("/")
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    fs.ls("/")
    fs.readContentFromFile("/a/b/c/d")
Output (including constructor and void operations):
    [None, [], None, None, ['a'], 'hello']

Example 2 — Append, search and delete
Input:
    fs.addContentToFile("/a/b/c/d", " world")
    fs.readContentFromFile("/a/b/c/d")
    fs.search("d")
    fs.delete("/a/b")
    fs.ls("/a")
    fs.search("d")
Output:
    None, 'hello world', ['/a/b/c/d'], None, [], []

Complexity (include string costs when discussing large inputs)
-------------------------------------------------------------
P = path length, K = directory children, C = file content length.
Path traversal / mkdir: O(P). ls: O(P + K log K), ignoring name-comparison length.
Append: O(P + existing content length + new content length), due to string copy.
Read: O(P), returning the existing string. delete: O(P) to detach the subtree;
Python may additionally spend O(subtree size + content size) reclaiming it.
Search: O(P + visited nodes + constructed path characters + result sorting).
Storage: O(nodes + names + content). Search keeps an explicit stack and results.
"""


class Node:
    def __init__(self):
        self.children = {}
        self.is_file = False
        self.content = ""


class FileSystem:
    def __init__(self):
        self.root = Node()

    def _find(self, path: str):
        # 从根目录逐层按名称查找；循环不会受到递归深度限制。
        node = self.root
        if path == "/":
            return node
        for name in path.split("/")[1:]:
            node = node.children[name]
        return node

    def ls(self, path: str) -> list[str]:
        node = self._find(path)
        if node.is_file:
            return [path.rsplit("/", 1)[1]]
        return sorted(node.children)

    def mkdir(self, path: str):
        node = self.root
        if path == "/":
            return
        for name in path.split("/")[1:]:
            if name not in node.children:
                node.children[name] = Node()
            node = node.children[name]

    def addContentToFile(self, filePath: str, content: str):
        parent_path, name = filePath.rsplit("/", 1)
        if parent_path == "":
            parent_path = "/"
        parent = self._find(parent_path)
        if name not in parent.children:
            parent.children[name] = Node()
            parent.children[name].is_file = True
        # ponytail: appends copy the string; use chunks if large repeated writes matter.
        parent.children[name].content += content

    def readContentFromFile(self, filePath: str) -> str:
        return self._find(filePath).content

    def delete(self, path: str):
        parent_path, name = path.rsplit("/", 1)
        if parent_path == "":
            parent_path = "/"
        parent = self._find(parent_path)
        del parent.children[name]

    def search(self, name: str, directory: str = "/") -> list[str]:
        # 路径查找只沿路径走；按名称搜索需要遍历指定子树。
        # ponytail: scan the subtree; add a name index if repeated global searches dominate.
        stack = [(directory, self._find(directory))]
        results = []
        while stack:
            path, node = stack.pop()
            for child_name, child in node.children.items():
                child_path = path.rstrip("/") + "/" + child_name
                if child_name == name:
                    results.append(child_path)
                if not child.is_file:
                    stack.append((child_path, child))
        return sorted(results)


if __name__ == "__main__":
    fs = FileSystem()
    print(fs.ls("/"))  # []
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    print(fs.ls("/"))  # ['a']
    print(fs.readContentFromFile("/a/b/c/d"))  # hello
    fs.addContentToFile("/a/b/c/d", " world")
    print(fs.readContentFromFile("/a/b/c/d"))  # hello world
    print(fs.ls("/a/b/c/d"))  # ['d']

    fs.addContentToFile("/z", "")
    fs.addContentToFile("/m", "root file")
    print(fs.ls("/"))  # ['a', 'm', 'z']
    print(fs.readContentFromFile("/z"))  # empty string (blank line)
    fs.mkdir("/a/b/c")
    print(fs.ls("/a/b/c"))  # ['d'] — existing content preserved

    fs.mkdir("/other/d")
    fs.addContentToFile("/other/d/d", "another")
    print(fs.search("d"))  # ['/a/b/c/d', '/other/d', '/other/d/d']
    print(fs.search("d", "/other/d"))  # ['/other/d/d'] — starting directory excluded
    print(fs.search("missing"))  # []

    fs.delete("/m")
    print(fs.ls("/"))  # ['a', 'other', 'z']
    fs.delete("/a/b")
    print(fs.ls("/a"))  # []
    print(fs.search("d"))  # ['/other/d', '/other/d/d']
    fs.mkdir("/a/b/c")
    print(fs.ls("/a/b/c"))  # [] — deleted content does not reappear

    deep = "/" + "/".join(["level"] * 1500)
    fs.mkdir(deep)
    fs.addContentToFile(deep + "/leaf", "deep file")
    print(fs.readContentFromFile(deep + "/leaf"))  # deep file
    print(fs.search("leaf") == [deep + "/leaf"])  # True
    fs.delete("/level")
    print(fs.search("leaf"))  # []
