class Class:
    def __init__(self):
        self.t = 0

    def func(self):
        def func1():
            return self.t

        def func2():
            return func1()
        return func2()


c = Class()

print(c.func())
