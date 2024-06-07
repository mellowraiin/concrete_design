
def x(var1):
    def y(var2):
        return var2+1
    a = y(3)
    def z(var3):
        return var3
    b=z(2)
    return a+var1+b

