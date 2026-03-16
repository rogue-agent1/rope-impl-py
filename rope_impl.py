"""Rope — efficient string operations for text editors."""
class Rope:
    def __init__(self, text="", left=None, right=None):
        self.left = left
        self.right = right
        self.text = text if not left and not right else ""
        self.weight = len(text) if not left else self._calc_weight(left)

    def _calc_weight(self, node):
        if node.text: return len(node.text)
        return node.weight + (self._calc_weight(node.right) if node.right else 0)

    def __len__(self):
        if self.text: return len(self.text)
        return len(self.left) + (len(self.right) if self.right else 0)

    def index(self, i):
        if self.text: return self.text[i]
        if i < self.weight: return self.left.index(i)
        return self.right.index(i - self.weight)

    def __str__(self):
        if self.text: return self.text
        return str(self.left) + (str(self.right) if self.right else "")

    @staticmethod
    def concat(r1, r2):
        return Rope(left=r1, right=r2)

    def split(self, i):
        if self.text:
            return Rope(self.text[:i]), Rope(self.text[i:])
        if i <= len(self.left):
            l1, l2 = self.left.split(i)
            return l1, Rope.concat(l2, self.right) if self.right else l2
        r1, r2 = self.right.split(i - len(self.left))
        return Rope.concat(self.left, r1), r2

    def insert(self, i, text):
        l, r = self.split(i)
        return Rope.concat(Rope.concat(l, Rope(text)), r)

    def delete(self, i, j):
        l, _ = self.split(i)
        _, r = self.split(j)
        return Rope.concat(l, r)

if __name__ == "__main__":
    r = Rope("Hello, ")
    r = Rope.concat(r, Rope("World!"))
    print(f"Rope: {r}")
    assert str(r) == "Hello, World!"
    assert len(r) == 13
    assert r.index(7) == "W"
    r = r.insert(7, "Beautiful ")
    print(f"After insert: {r}")
    assert str(r) == "Hello, Beautiful World!"
    r = r.delete(7, 17)
    print(f"After delete: {r}")
    assert str(r) == "Hello, World!"
    print("All tests passed!")
