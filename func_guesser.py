def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class FuncGuesser:
    def __init__(self, y_obj, y_tol, verbose=False):
        self.p0 = self.p1 = self.pr = None
        self.y_obj = y_obj
        self.y_tol = y_tol

        self.verbose = verbose
    
    def eval(self, x, y):
        if self.verbose:
            print(f'eval({x}) = {y}')

        p = Point(x, y)
        if abs(p.y - self.y_obj) < self.y_tol:
            self.pr = p
        elif self.p0 is None:
            self.p0 = p
        elif self.p1 is None:
            self.p1 = p
        else:
            if sign(y - self.y_obj) != sign(self.p0.y - self.y_obj):
                self.p1 = p
            elif sign(y - self.y_obj) != sign(self.p1.y - self.y_obj):
                self.p0 = p
            else:
                raise Exception('error bracketing zero')


    def has_result(self):
        return self.pr is not None
    

    def result(self):
        return self.pr


    def guess(self):
        if self.p0 is not None and self.p1 is not None:
            return (self.p0.x + self.p1.x) / 2
        else:
            raise Exception('need to evaluate 2 starting endpoints')