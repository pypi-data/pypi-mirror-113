from pyctlib import vector, totuple

class MimcMatrix:

    def __init__(self, *args, symbol="x"):
        args = totuple(args)
        self.shape = args
        self.content = vector.meshgrid(vector(args).map(lambda n: vector.range(1, n + 1))).map(lambda loc: "{}[{}]".format(symbol, ",".join(str(l) for l in loc))).reshape(args)

    def __str__(self):
        return str(self.content)

    @property
    def T(self):
        return self.content.tr
