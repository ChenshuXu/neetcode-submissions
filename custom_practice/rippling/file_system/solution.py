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
    """树中的一个节点：可以是目录，也可以是文件，不对应真实磁盘上的对象。"""

    def __init__(self):
        # children 的结构是 dict[str, Node]：
        # key 是直接子项的名字（如 "b" 或 "readme"），不是完整路径；
        # value 是对应的 Node 对象，不是文件内容，也不是另一个裸 dictionary。
        # 例如 /a 下有目录 b 和文件 readme：
        # a_node.children = {"b": b_node, "readme": readme_node}
        # b_node.children 再保存 b 自己的子项，逐层连接形成一棵树。
        # 每个 Node 都有自己的字典；文件节点的 children 始终为空。
        self.children = {}
        # 新节点默认是目录；创建文件时显式改成 True。
        # 不能用 children 是否为空判断类型，因为空目录和文件都没有孩子。
        self.is_file = False
        # 文件的完整文本，类型为 str；目录不使用这个字段，保持空字符串。
        # 空文件的 content 也是 ""，所以也不能靠 content 判断节点类型。
        self.content = ""


class FileSystem:
    def __init__(self):
        # root 是代表 "/" 的目录 Node，是所有路径查找的起点。
        # Node 不保存自己的名字或完整路径；名字保存在父节点的 children key 中。
        self.root = Node()

    def _find(self, path: str):
        """返回路径对应的 Node 对象本身；不会创建节点，也不返回内容或路径字符串。"""
        # 从根目录逐层按名称查找；循环不会受到递归深度限制。
        node = self.root
        if path == "/":
            return node
        # "/a/b".split("/") 得到 ["", "a", "b"]，[1:] 去掉开头空字符串。
        # node 始终指向当前已走到的节点：root -> a_node -> b_node。
        # 输入保证路径存在，且中间节点都是目录，因此可以直接按 key 取孩子。
        for name in path.split("/")[1:]:
            node = node.children[name]
        return node

    def ls(self, path: str) -> list[str]:
        """返回名称列表：文件返回 [文件名]；目录返回按字典序排列的直接子项名。"""
        node = self._find(path)
        if node.is_file:
            # 从右边只切一次："/a/b/readme" -> ["/a/b", "readme"]。
            return [path.rsplit("/", 1)[1]]
        # 遍历 dictionary 默认取得 keys；这里排序的是名称，不是 Node 对象。
        # 只列当前目录这一层，不递归列出后代；空目录返回 []。
        return sorted(node.children)

    def mkdir(self, path: str):
        """逐层创建缺失目录，保留已有节点及内容；返回 None。"""
        node = self.root
        if path == "/":
            return
        for name in path.split("/")[1:]:
            # 当前目录缺少这个孩子时，才创建默认的目录 Node。
            # 例如创建 /a/b/c，可以在同一次循环中依次补齐 a、b、c。
            if name not in node.children:
                node.children[name] = Node()
            # 无论刚创建还是原本存在，都进入这个子目录，继续处理下一段路径。
            node = node.children[name]

    def addContentToFile(self, filePath: str, content: str):
        """文件不存在则创建，否则在末尾追加 content；返回 None。父目录保证存在。"""
        # 拆出父目录路径和文件名，例如 /a/note -> ("/a", "note")。
        parent_path, name = filePath.rsplit("/", 1)
        # 根目录下的 /note 会拆成 ("", "note")，空的父路径要改为 "/"。
        if parent_path == "":
            parent_path = "/"
        parent = self._find(parent_path)
        if name not in parent.children:
            # 文件也是 Node，只是类型标记不同；它的 children 保持为空。
            parent.children[name] = Node()
            parent.children[name].is_file = True
        # 修改树里已有的那个文件对象；+= 保留旧内容并追加新内容，不是覆盖。
        # ponytail: appends copy the string; use chunks if large repeated writes matter.
        parent.children[name].content += content

    def readContentFromFile(self, filePath: str) -> str:
        """返回文件的完整字符串内容；空文件返回 ""，不修改文件。"""
        return self._find(filePath).content

    def delete(self, path: str):
        """移除文件或整个目录子树；返回 None。输入保证目标存在且不是根目录。"""
        # 必须找到父目录，因为指向目标节点的那条连接保存在父目录的字典中。
        parent_path, name = path.rsplit("/", 1)
        if parent_path == "":
            parent_path = "/"
        parent = self._find(parent_path)
        # 删除一个 key 就切断了父节点到目标的连接。
        # 若目标是目录，其后代也无法再从 root 到达，不必逐个遍历删除。
        # 这不是清空目标的 content；Python 会在对象不再被引用时回收它们。
        del parent.children[name]

    def search(self, name: str, directory: str = "/") -> list[str]:
        """返回指定目录后代中所有同名文件/目录的绝对路径，排序后返回；无匹配返回 []。"""
        # 路径查找只沿路径走；按名称搜索需要遍历指定子树。
        # ponytail: scan the subtree; add a name index if repeated global searches dominate.
        # stack 是 list[tuple[str, Node]]，每一项为 (目录的绝对路径, 目录节点)。
        # 例如 [("/a", a_node)]；存路径是因为 Node 本身没有完整路径字段。
        # 使用后进先出的显式栈进行深度优先遍历，避免深层目录触发递归深度限制。
        stack = [(directory, self._find(directory))]
        # results 是 list[str]，只保存匹配项的绝对路径，不保存 Node 对象。
        results = []
        while stack:
            path, node = stack.pop()
            # items() 取出每个直接孩子的 (名称, Node 对象)。
            # 只检查孩子，不检查当前节点，因此起始目录本身不计入结果。
            for child_name, child in node.children.items():
                # 根路径 "/" 先去掉尾部斜线，避免拼成 "//a"；普通路径拼成 "/a/b"。
                child_path = path.rstrip("/") + "/" + child_name
                # 比较的是 basename 的完全相等，不是完整路径或子串匹配。
                # 文件和目录都可以命中，所以这一步放在类型判断之前。
                if child_name == name:
                    results.append(child_path)
                # 文件没有孩子，不需要入栈；目录即使命中也继续搜索其后代。
                if not child.is_file:
                    stack.append((child_path, child))
        # 遍历顺序不保证字典序，所以最后统一排序。
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
