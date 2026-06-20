class Solution:

    def encode(self, strs: List[str]) -> str:
        res = ""
        for s in strs:
            length = len(s)
            res += str(length) + "#" + s
        return res

    def decode(self, s: str) -> List[str]:
        res = []
        i = 0
        while i < len(s):
            length_str = ""
            while s[i] != '#':
                length_str += s[i]
                i += 1
            length = int(length_str)
            i += 1
            begin = i
            end = i + length
            res.append(s[begin:end])
            i = end
        return res