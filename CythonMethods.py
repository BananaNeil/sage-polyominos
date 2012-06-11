%cython
cdef extern from "stdlib.h":
    int c_abs "abs"(int i)

cpdef rotate2_cy(self,int direction):
    cdef list newP = []
    cdef int i = 0, h = 0, w = 0
    newPiece = self.__copy__()
    for i in range(abs(direction)):
        newP = [[newPiece._p[h][w] for h in range(len(newPiece._p))][::-(abs(direction)/direction)] for w in range(len(newPiece._p[0]))][::(abs(direction)/direction)]
        newPiece = self.createPolyomino(newP,self._color)
        newPiece._height = len(newPiece._p)
        newPiece._width = len(newPiece[0])
    return newPiece

cpdef eq_cy(self,other):
    if not (self._width==other._width and self._height==other._height):
        return False
    cdef int h, w
    for h in range(len(self._p)):
        for w in range(len(self._p[0])):
            if not self._p[h][w]/self._color==other._p[h][w]/other._color:
                return False
    return True
