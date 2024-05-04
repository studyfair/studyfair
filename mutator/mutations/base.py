class Base:
    def __init__(self, source_tree, randomizer):
        self.source_tree = source_tree
        self.randomizer = randomizer

    def call(self):
        raise NotImplementedError

    def __visit(self, visitor: cst.CSTVisitor):
        self.source_tree.visit(visitor)
