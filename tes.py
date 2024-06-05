
def x(var1):
    def y(var2):
        return var2+1
    z = y(3)
    return z+var1



print(x(1))
