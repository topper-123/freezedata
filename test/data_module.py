class Test:
    a = 1
    def __init__(self, *args):
        self.b = list(args)

t = Test(1, 2, 3)