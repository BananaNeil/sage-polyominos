class Polyomino:
    def __init__ (self , piece=[], color=1):
        self._p = copy(piece)
        self._color = color
        self.setColor(color)
        self._height = len(self._p)
        self._width = 0 if self._height==0 else len(self._p[0])
        self._length = int(sum(flatten(self._p))/self._color)
        
    def __len__ (self):
        return int(self._length)
        
    def __eq__ (self,other):
        return eq_cy(self,other)
    
    def __lt__(self, other):
        return (self._height>other._height) if (self._width-other._width)==0 else self._width<other._width
        
    def __gt__(self, other):
        return (self._height<other._height) if (self._width-other._width)==0 else self._width>other._width
        
    def __le__(self, other):
        return (self._height>=other._height) if (self._width-other._width)==0 else self._width<=other._width
        
    def __ge__(self, other):
        return (self._height<=other._height) if (self._width-other._width)==0 else self._width>=other._width
        
    def __ne__(self, other):
        return not self == other
        
    def __add__ (self,other):
        s = PolyominoSet()
        s.addPiece(self)
        s.addPiece(other)
        return s
        
    def __str__(self):
        color = (self._color-1)%(len(PolyominoColorDictStr))
        string = ""
        for h in range(len(self._p)):
            string += "\n"
            for w in range(len(self._p[0])):
                string += PolyominoColorDictStr[color] if self[h][w]!=0 else " "
                string += " "
        return string 
        
    def __repr__(self):
        return str(self._p)
        
    def __copy__(self):
        return Polyomino([[self._p[h][w] for w in range(len(self._p[0]))] for h in range(len(self._p))],self._color)
        
    def __getitem__(self,n):
        return self._p[n]
        
    def _isConnected(self,h,w):
        return ((h+1<len(self._p) and  not self._p[h+1][w]==0) or (w+1<len(self._p[0]) and not self._p[h][w+1]==0) or (w-1>=0 and not self._p[h][w-1]==0) or (h-1>=0 and not self._p[h-1][w]==0))
       
    def isCompatibleWith(self,other,traceBack=false):
        if len(self)<len(other):
            temp = self
            self = other
            other = temp
        g1 = PolyominoGrid(self)
        g2 = PolyominoGrid(other)
        a = g1.width+g1.height
        gridList1 = [[] for i in range(a +1)]
        gridList1[a] = [g1]
        a = g2.width+g2.height
        gridList2 = [[] for i in range(a +1)]
        gridList2[a] = [g2]
        foundOne = false
        lcm = Integer(len(self))._lcm(Integer(len(other)))
        answer = None
        firstTimeThrough = true
        while answer is None:
            if len(self)!=len(other):
                NumOfComps1 = lcm/len(self)-1 if firstTimeThrough else lcm/len(self)
                NumOfComps2 = lcm/len(other)-1 if firstTimeThrough else lcm/len(other)
                firstTimeThrough = false
            else:
                NumOfComps1 = 1
                NumOfComps2 = 1
            for i in range(NumOfComps1):
                gridList1 = self._isCompatibleWith2(self,gridList1,traceBack=traceBack)
            if traceBack:
                print "first guy done"
            for i in range(NumOfComps2-1):
                gridList2 = self._isCompatibleWith2(other,gridList2)
            gridList2 = self._isCompatibleWith2(other,gridList2,gridList1,traceBack=traceBack)
            if traceBack:
                print "second guy done"
            if not type(gridList2[0])==list:
                answer = gridList2
            elif traceBack:
                    print "Cross checked"
        return answer
        
    def _isCompatibleWith2(self,obj,gridList,newGridList2=None,traceBack=false):
        symmetric = obj.isSymmetricH() and obj.isSymmetricV()
        rotations = 1 if symmetric and obj.isSymmetricR() else (2 if symmetric else 4)
        newGridList = []
        for lists in gridList:
            for grid in lists:
                if traceBack:
                    print grid
                for i in range(rotations):
                    obj = obj.rotate()
                    obj_filled_spaces = obj.filledSpaces()
                    grid_open_spaces = grid.openSpaces()
                    for a in obj_filled_spaces:
                        for b in grid_open_spaces:
                            g = copy(grid).addPiece(obj,a[0],a[1],b[0],b[1])
                            if not g is None:
                                k = g.width+g.height
                                for i in range(k-len(newGridList)+1):
                                    newGridList.append([])
                                currentList = newGridList[k]
                                if not g in currentList:
                                    if not newGridList2 is None:
                                        if k<len(newGridList2):
                                            for g2 in newGridList2[k]:
                                                if g2==g:
                                                    return [g,g2]
                                    currentList.append(g)
        return newGridList
        
    def filledSpaces(self):
        newP = copy(self)
        return [[h,w] for w in range(newP.getWidth()) for h in range(newP.getHeight()) if newP[h][w]!=0]
        
    def openSpaces(self,expand=true):
        newP = copy(self)
        if expand:
            newP.insertRow(0)
            newP.insertRow()
            newP.insertColumn(0)
            newP.insertColumn()
            return [[h-1,w-1] for w in range(newP.getWidth()) for h in range(newP.getHeight()) if newP[h][w]==0 and newP._isConnected(h,w)]
        return [[h,w] for w in range(newP.getWidth()) for h in range(newP.getHeight()) if newP[h][w]==0 and newP._isConnected(h,w)]
        
    def insertColumn(self,index=None,column=None,newCopy=false):
        if column is None:
            column = [0 for i in range(len(self._p))]
        if index is None:
            index = self._width
        elif not len(column)==len(self._p):
            raise AttributeError, "Column must have a length of "+self.getWidth()+" to be compatible with this polyomino."
        newP = copy(self) if newCopy else self
        newP._p = [[self._p[h][w] for w in range(len(self._p[0]))][:index]+[column[h]]+[self._p[h][w] for w in range(len(self._p[0]))][index:] for h in range(len(self._p))]
        newP.setColor(self._color)
        newP._width += 1
        newP._length += sum([1 for i in column if not i==0])
        return newP
        
    def insertRow(self,index=None,row=None,newCopy=false):
        if row is None:
            row = [0 for i in range(len(self._p[0]))]
        if index is None:
            index = self._height
        elif not len(row)==len(self._p[0]):
            raise AttributeError, "Row must have a length of "+srt(self.getWidth())+" to be compatible with this polyomino."
        newP = copy(self) if newCopy else self
        newP._p.insert(index,row)
        newP.setColor(self._color)
        newP._height += 1
        newP._length += sum(newP[index])/newP._color
        return newP
        
    def rotate(self,direction=1):
        return rotate2_cy(self,direction)
        
    def setColor(self,color=1,RGBtuple=None):
        if RGBtuple is None:
            if color in PolyominoColorDict:
                RGBtuple = PolyominoColorDict.get(color)
            else:
                import random
                a = floor(random.random()*255)
                t = [255,a,0]
                random.shuffle(t)
                RGBtuple = tuple(t)
        PolyominoColorDict[color] = RGBtuple
        self._p = [[(0 if self._p[h][w]==0 else color) for w in range(len(self._p[0]))] for h in range(len(self._p))]
        self._color = color
        
    def getColorNum(self):
        return self._color
        
    def getColorRGB(self):
        return PolyominoColorDict.get(self._color)
        
    def getColorStr(self):
        color = (self._color-1)%(len(PolyominoColorDictStr))
        return PolyominoColorDictStr[color]
        
    def getWidth(self):
        return self._width
        
    def getHeight(self):
        return self._height
        
    def getXY(self,x,y):
        return self._p[y][x]
        
    def addXY(self,x,y):
        newP = self
        newP._p[y][x] = newP._color
        newP._length += 1
        return newP
        
    def flipV(self):
        return Polyomino(self._p[::-1],self._color)
        
    def flipH(self):
        return Polyomino([self._p[h][::-1] for h in range(len(self._p))], self._color)
        
    def isSymmetricV(self):
        return self == self.flipV()
        
    def isSymmetricH(self):
        return self == self.flipH()
        
    def isSymmetricR(self,n=1):
        return self == self.rotate(n)
        
    def isSymmetric(self):
        return self.isSymmetricV() and self.isSymmetricH()
        
    def hasHole(self):
        for h in range(1,self._height-1):
            for w in range(1,self._width-1):
                if self._p[h][w]==0 and not (self._p[h+1][w]==0 or self._p[h-1][w]==0 or self._p[h][w+1]==0 or self._p[h][w-1]==0):
                    return true
        return false
    
    def createPolyomino(self,grid=None,color=1):
        grid = self._p if grid is None else grid
        return Polyomino(copy(grid),color)
        
        
    def generateDrawingJS(self,cellID,size,border_width,xPos,yPos):
        return r"""
                var cellID = %s;
                var P = %s;
                var height = %s;
                var width = %s;
                var SQUARE_SIZE = %s;
                var BORDER_WIDTH = %s;
                var xPos = %s;
                var yPos = %s;
                var color = '%s';
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                var context = drawingBox.getContext('2d');
                //document.getElementById('drawing_on_cell_'+cellID).innerHTML = P;
                for (h=0;h<height;h++){
                    for (w=0;w<width;w++){
                        context.fillStyle = color;
                        context.lineWidth = BORDER_WIDTH;
                        context.strokeStyle = "rgb(0,0,0)";
                        
                        if (P[h][w]!=0){                        
                            context.fillRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, SQUARE_SIZE);
                            if(InnerBorder==1){
                                context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, SQUARE_SIZE);
                            } else if (OuterBorder==1){
                                //left
                                if (w==0 || P[h][w-1]==0){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), 0, SQUARE_SIZE);
                                }
                                //right
                                if (w==width-1 || P[h][w+1]==0){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*(w+1)), yPos+((SQUARE_SIZE)*h), 0, SQUARE_SIZE);
                                }
                                //top
                                if (h==0 || P[h-1][w]==0){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, 0);
                                }
                                //bottom
                                if (h==height-1 || P[h+1][w]==0){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*(h+1)), SQUARE_SIZE, 0);
                                }
                            }
                        }
                    }
                }
        """%(cellID,self._p,self.getHeight(),self.getWidth(),size,border_width,xPos,yPos,"rgb"+str(PolyominoColorDict.get(self._color)))
        
    def draw(self,size=35,borderWidth=None,padding=20,innerBorder=false,outerBorder=true,cellID=None,boxBorder=2):
        if borderWidth is None:
            borderWidth = size*.09
        if cellID is None:
            buildNewCanvas = true
            cellID = sagenb.notebook.interact.SAGE_CELL_ID
        else:
            buildNewCanvas = false
        innerBorder = 1 if innerBorder else 0
        outerBorder = 1 if outerBorder else 0
        innerDrawingJS = self.generateDrawingJS(cellID,size,borderWidth,padding,padding)
        s = r"""
            <canvas id='drawing_on_cell_%s'>
            Your browser does not support this awesome feature. You should probably go download firefox 3+ now.
            </canvas>
            <SCRIPT type="text/javascript">
            var cellID = %s;
            var P = %s;
            var padding = %s;
            var SQUARE_SIZE = %s;
            var BORDER_WIDTH = %s;
            var height = %s;
            var width = %s;
            var InnerBorder = %s;
            var OuterBorder = %s;
            var boxBorder = %s
            loaded = function(){
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                drawingBox.setAttribute('width',2*padding+SQUARE_SIZE*(width));
                drawingBox.setAttribute('height',2*padding+SQUARE_SIZE*(height));
                drawingBox.style.border=boxBorder+'px solid black';
            }
            drawSquares = function(){
                %s
            }
            setTimeout(loaded, 200);
            setTimeout(drawSquares, 600); 
            </SCRIPT>"""%(cellID,cellID,self._p,padding,size,borderWidth,self.getHeight(),self.getWidth(),innerBorder,outerBorder,boxBorder,innerDrawingJS)
        return html(s)
