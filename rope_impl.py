"""Rope — efficient string operations for text editors."""
class Rope:
    def __init__(self, text=""):
        self.text = text
        self.left = None
        self.right = None

    def __len__(self):
        if self.text is not None and self.left is None:
            return len(self.text)
        l = len(self.left) if self.left else 0
        r = len(self.right) if self.right else 0
        return l + r

    def index(self, i):
        if self.text is not None and self.left is None:
            return self.text[i]
        ll = len(self.left) if self.left else 0
        if i < ll:
            return self.left.index(i)
        return self.right.index(i - ll)

    def __str__(self):
        if self.text is not None and self.left is None:
            return self.text
        return str(self.left or "") + str(self.right or "")

    @staticmethod
    def concat(r1, r2):
        node = Rope.__new__(Rope)
        node.text = None
        node.left = r1
        node.right = r2
        return node

    def split(self, i):
        if self.text is not None and self.left is None:
            return Rope(self.text[:i]), Rope(self.text[i:])
        ll = len(self.left) if self.left else 0
        if i <= ll:
            l1, l2 = self.left.split(i)
            return l1, Rope.concat(l2, self.right) if self.right else l2
        r1, r2 = self.right.split(i - ll)
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
