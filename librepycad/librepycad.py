import os
class CADFile:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def add(self, item):
        # print(type(item))
        if type(item) == tuple:
            for i in item:
                # print("appending from tuple: {}".format(i))
                self.elts.append(i)
        else:
            # print("appending: {}".format(item))
            self.elts.append(item)

    def __enter__(self):
        self.elts = []
        return self

    def __exit__(self, type, value, traceback):
        with open(self.name+".lpc", 'w') as w:
            w.write("clear\n")
            c = 0
            for elt in self.elts:
                c += 1
                w.write(elt())
            w.write("kill\n")
        print("{} elts written to {}".format(c, self.name))

class Project:
    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def __enter__(self):
        self.oldDir = os.getcwd()
        os.chdir(self.path)
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.oldDir)

class Command:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs



    def __call__(self):
        return "unimplemented command"

class PO(Command):
    def __init__(self, pt):
        self.pt = pt

    def __call__(self):
        return "po\n{}\n".format(self.pt())

class L(Command):
    def __init__(self, *args):
        self.pts = args#[a() for a in args]
    def __call__(self):
        s = "l\n"
        for pt in self.pts:
            s += pt()
            s += "\n"
        return s

class PL(Command):
    def __init__(self, point_list):
        """
        point_list: a list point strings
        """
        self.point_list = point_list
    def __call__(self):
        s = 'pl\n'
        for p in self.point_list:
            s += "{}\n".format(p())
        s += "close\n"
        return s

class Arc(Command):
    def __init__(self, *args, center=False):
        self.center=center
        self.args = [arg() if type(arg)==Coord else arg for arg in args ]

    def __call__(self):
        s = "arc\n"
        if self.center:
            s += "center\n"
            s += "{}\n{}\n{}\n{}\n".format(*self.args[:4])
        else:
            s += "{}\n{}\n{}\n".format(*self.args[:3])
        return s

class Circle(Command):
    def __init__(self, c, r):
        self.c = c
        self.r = r

    def __call__(self):
        s = "circle\n{}\n{}\n".format(self.c(), self.r)
        return s

class Rectangle(Command):
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
    def __call__(self):
        s = "rectangle\n{}\n{}\n".format(self.c1(), self.c2())
        return s

class Dimension(Command):
    def __init__(self,d1, d2, d3):
        self.com = None
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
    def __call__(self):
        s = "{}\n{}\n{}\n{}\n".format(self.com, self.d1(), self.d2(), self.d3())
        return s

class Da(Dimension):
    def __init__(self, *args):
        super().__init__(*args)
        self.com = "da"

class Dr(Dimension):
    def __init__(self, *args):
        super().__init__(*args)
        self.com = "dr"

class Dh(Dimension):
    def __init__(self, *args):
        super().__init__(*args)
        self.com = "dh"


class Coord:
    def __init__(self, x, y, *args):
        self.x = x
        self.y = y
        self.rel = "rel" in args
        self.ang = "ang" in args

    def __call__(self):
        sep = "," if not self.ang else "<"
        pre = "" if not self.rel else "@"
        return "{}{}{}{}".format(pre, self.x, sep, self.y)

class RadiusBox:
    def __init__(self, c1, c2, r,
                 draw_sides=(True, True, True, True),
                 draw_arcs=(True, True, True, True),
                 mirror_arcs=(False ,False, False, False, False, False, False, False)):
        self.c1 = c1
        self.c2 = c2
        self.r = r
        self.ds = draw_sides
        self.da = draw_arcs
        self.ma = mirror_arcs


    def __call__(self):
        elts = []
        # left side
        if self.ds[3]: elts.append(L(Coord(self.c1.x,self.c1.y+self.r),Coord(self.c1.x, self.c2.y-self.r)))
        # right side
        if self.ds[1]: elts.append(L(Coord(self.c2.x,self.c1.y+self.r),Coord(self.c2.x, self.c2.y-self.r)))
        # top
        if self.ds[2]: elts.append(L(Coord(self.c1.x+self.r,self.c1.y),Coord(self.c2.x-self.r, self.c1.y)))
        # bottom
        if self.ds[0]: elts.append(L(Coord(self.c1.x+self.r,self.c2.y),Coord(self.c2.x-self.r, self.c2.y)))

        # left bottom
        if self.da[2]:
            if self.ma[4]:
                elts.append(Arc(Coord(self.c1.x+self.r, self.c1.y-self.r), self.r, 90, 180, center=True))
            elif self.ma[5]:
                elts.append(Arc(Coord(self.c1.x-self.r, self.c1.y+self.r), self.r, -90, 0, center=True))
            else:
                elts.append(Arc(Coord(self.c1.x+self.r, self.c1.y+self.r), self.r, -180, -90, center=True))
        # left top
        if self.da[3]:
            if self.ma[6]:
                elts.append(Arc(Coord(self.c1.x-self.r, self.c2.y-self.r), self.r, 0, 90, center=True))
            elif self.ma[7]:
                elts.append(Arc(Coord(self.c1.x+self.r, self.c2.y+self.r), self.r, -180, -90, center=True))
            else:
                elts.append(Arc(Coord(self.c1.x+self.r, self.c2.y-self.r), self.r, 90, 180, center=True))
        # right bottom
        if self.da[1]:
            if self.ma[2]:
                elts.append(Arc(Coord(self.c2.x+self.r, self.c1.y+self.r), self.r, -180, -90, center=True))
            elif self.ma[3]:
                elts.append(Arc(Coord(self.c2.x-self.r, self.c1.y-self.r), self.r, 0, 90, center=True))
            else:
                elts.append(Arc(Coord(self.c2.x-self.r, self.c1.y+self.r), self.r, -90, 0, center=True))
        # right top
        if self.da[0]:
            if self.ma[0]:
                elts.append(Arc(Coord(self.c2.x-self.r, self.c2.y+self.r), self.r, -90, 0, center=True))
            elif self.ma[1]:
                elts.append(Arc(Coord(self.c2.x+self.r, self.c2.y-self.r), self.r, 90, 180, center=True))
            else:
                elts.append(Arc(Coord(self.c2.x-self.r, self.c2.y-self.r), self.r, 0, 90, center=True))


        return "\n".join([elt() for elt in elts])

class RadiusPL:
    def __init__(self, r, *args):
        self.r = r
        self.pts = args
