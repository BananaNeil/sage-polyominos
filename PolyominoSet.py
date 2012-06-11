class PolyominoSet:
    def __init__ (self, set=None):
        self.r = r
        self.pieceSeperator = ":"
        self.printNums = false
        self.printSquares = true
        self.set = []
        self._keySet = []
        if set is None:
            pass
        elif type(set)==list:
            if type(set[0])==list:
                if type(set[0][0])==list:                                    #list of polyomino lists
                    set = [Polyomino(p,mean([i for i in p[0] if i!=0])) for p in set]
                    self.set = [copy(set[i]) for i in range(len(set))]
                else:                                                        #single polyomino list
                    self.addPiece(set)
            elif type(set[0])==int or type(set[0])==Integer:                 #list of ints
                self.addSet(set)
            else:                                                            #List of polyominos
                self.set = [copy(set[i]) for i in range(len(set))]
        elif type(set)==int or type(set)==Integer:                           #single int
                self.addSet(set)
        else:                                                                #single polyomino
            set = [set]
            self.set = [copy(set[i]) for i in range(len(set))]
        
    def __getitem__(self,n):
        return self.set[n]
        
    def __add__(self,other):
        return PolyominoSet(self.set + other.set)
        
    def __sub__(self,other):
        return PolyominoSet([i for i in self.set if not (i in other.set)])
        
    def __mul__(self,n):
        return PolyominoSet(copy(self.set)*n)
        
    def __len__(self):
        return len(self.set)
        
    def __repr__(self):
        return str(self.set)
        
    def __str__(self):
        if self.printNums==self.printSquares:
            self.printSquares = false
        if self.set == []:
            return "empty"
        s = ""
        for h in range(self.maxHeight()):
            s += self.pieceSeperator+"  "
            for a in self.set:
                for w in range(a.getWidth()):
                    if a.getHeight()>h:
                        s += ("  " if a[h][w]==0 else (a.getColorStr() if self.printSquares else str(a[h][w]))+" ")
                    else:
                        s += "  "
                s += " "+self.pieceSeperator+"  "
            s += "\n"
        return s
    
    def Print(self):
        print '<html><!-- notruncated -->'
        print str(self)
        print '</html>'
        
    def strSettings(self, *args , **kwds):
        for i in kwds.keys():
            if type(kwds.get(i))==str:
                exec "self."+str(i)+" = '"+str(kwds.get(i))+"'"
            else:
                exec "self."+str(i)+" = "+str(kwds.get(i))
        
    def __copy__(self):
        return PolyominoSet([copy(p) for p in self.set])
        
    def maxHeight(self):
        maxH = max([len(p._p) for p in self.set])
        return maxH
        
    def maxWidth(self):
        maxW = max([len(p._p[0]) for p in self.set])
        return maxW
        
    def genSet(self,n,filters=[],fixed=false,p=[[1]]):
        self.set = []
        self.addSet(n,filters,fixed,p)
        
    def addSet(self,n,filters=[],fixed=false,p=[[1]]):
        if (type(p) == list):
            p=Polyomino(p)
        if (type(n) != list):
            n=[n]
        for i in n:
            self.genSet2(i,filters,fixed,p)
        
    def genSet2(self,n,filters,fixed,p):
        if not (type(filters) == list):
            filters = [filters]
        if len(p)==n:
            fs = []
            for f in filters:
                exec "fs.append("+f+")"
            if not (false in fs):
                self.addPiece(p,fixed,false)
        else:
            blankH = [0 for i in range(0,p.getWidth())]
            #inner
            openSpaces = [[h,w] for w in range(p.getWidth()) for h in range(p.getHeight()) if p[h][w]==0 and p._isConnected(h,w)]
            for a in openSpaces:
                self.genSet2(n,filters,fixed,copy(p).addXY(a[1],a[0]))
            #top
            openSpaces = [[0,w] for w in range(len(p[0])) if not p[0][w]==0]
            for a in openSpaces:
                newRow = [1 if w==a[1] else 0 for w in range(len(p[0]))]
                self.genSet2(n,filters,fixed,p.insertRow(a[0],newRow,true))
            symmetric = p.isSymmetricH() and p.isSymmetricV()
            if (not (symmetric and p.isSymmetricR())) or fixed:
                #left
                openSpaces = [[0,h] for h in range(p.getHeight()) if not p[h][0]==0]
                for a in openSpaces:
                    newColumn = [1 if h==a[1] else 0 for h in range(p.getHeight())]
                    self.genSet2(n,filters,fixed,p.insertColumn(a[0],newColumn,true))
            if (not symmetric) or fixed:
                #bottom
                openSpaces = [[p.getHeight(),w] for w in range(len(p[0])) if not p[p.getHeight()-1][w]==0]
                for a in openSpaces:
                    newRow = [1 if w==a[1] else 0 for w in range(len(p[0]))]
                    self.genSet2(n,filters,fixed,p.insertRow(a[0],newRow,true))
                #right
                openSpaces = [[p.getWidth(),h] for h in range(p.getHeight()) if not p[h][p.getWidth()-1]==0]
                for a in openSpaces:
                    newColumn = [1 if h==a[1] else 0 for h in range(p.getHeight())]
                    self.genSet2(n,filters,fixed,p.insertColumn(a[0],newColumn,true))
                    
    def addPiece(self,p,fixed=false,duplicates=true):
        if (type(p) == list):
            p=Polyomino(p)
        p.setColor(len(self.set)+1)
        skip = false
        if (not duplicates) and (p in self._keySet):
            skip = true
        if skip==false:
            self.set.append(p)
            newP = p
            if (not fixed):
                symmetric = p.isSymmetricH() and p.isSymmetricV()
                rotations = 1 if symmetric and p.isSymmetricR() else (2 if symmetric else 4)
                for i in range(rotations):
                    newP = newP.rotate()
                    self._keySet.append(newP)
            else:
                self._keySet.append(newP)
                
    def makeTall(self):
        for i in range(len(self.set)):
            if self.set[i].getHeight()<self.set[i].getWidth():
                self.set[i] = self.set[i].rotate()
                
    def makeWide(self):
        for i in range(len(self.set)):
            if self.set[i].getHeight()>self.set[i].getWidth():
                self.set[i] = self.set[i].rotate()
                
    def setColor(self,n):
        for p in self.set:
            p.setColor(n)
                
    def clearSet(self):
        self.set = []
                
    def movePiece(self,index,newIndex):
        myPiece = self.set[index]
        self.set = self.set[:index]+self.set[index+1:]
        self.set = self.set[:newIndex]+[myPiece]+self.set[newIndex:]
         
    def sort(self,criteria="width",ascending=true,descending=false):
        if ascending and descending:
            ascending = false
        ascending = 1 if ascending else -1
        self.set.sort()
        if not criteria == "width":
            d=[]
            pieceLength = max([p.getHeight() for p in self.set])
            for i in range(pieceLength):
                if criteria == "height":
                    d += [p for p in self.set if p.getHeight()==i+1]
                if criteria == "thickness":
                    d += [p for p in self.set if min(p.getHeight(),p.getWidth())==i+1]
                if criteria == "color":
                    d += [p for p in self.set if p.getColor()==i+1]
                if criteria == "squareCount" or criteria == "length":
                    d += [p for p in self.set if len(p)==i+1]
            self.set = d
        self.set = self.set[::ascending]
            
    def execFunction(s):
        exec s
        
    def draw(self,size=35,borderWidth=None,padding=20,innerBorder=false,outerBorder=true,cellID=None,boxBorder=2,boxMaxWidth=900):
        if borderWidth is None:
            borderWidth = size*.09
        if cellID is None:
            buildNewCanvas = true
            cellID = sagenb.notebook.interact.SAGE_CELL_ID
        else:
            buildNewCanvas = false
        innerBorder = 1 if innerBorder else 0
        outerBorder = 1 if outerBorder else 0
        boxCurrentWidth = padding
        boxWidth = 0
        piecesToDraw = [[]]
        maxHeights = []
        maxWidths = [[]]
        innerDrawingJS = ""
        for p in self.set: 
            if boxCurrentWidth+p.getWidth()*size+padding>boxMaxWidth:
                maxHeights.append(max([a.getHeight() for a in piecesToDraw[-1]]))
                piecesToDraw.append([])
                maxWidths.append([])
                boxWidth = max(boxWidth,boxCurrentWidth+padding)
                boxCurrentWidth = 0
            piecesToDraw[-1].append(p)
            maxWidths[-1].append(p.getWidth())
            boxCurrentWidth += p.getWidth()*size+padding
        boxWidth = max(boxWidth,boxCurrentWidth+padding)
        maxHeights.append(max([a.getHeight() for a in piecesToDraw[-1]]))
        #for i in range(len(piecesToDraw)):
        #    for j in range(3):
        #s = piecesToDraw[2][0]
        #innerDrawingJS += s.generateDrawingJS(cellID,size,borderWidth,padding,padding)
        for i in range(len(piecesToDraw)):
            for j in range(len(piecesToDraw[i])):
                s = piecesToDraw[i][j]
                innerDrawingJS += s.generateDrawingJS(cellID,size,borderWidth,sum(maxWidths[i][:j])*size+padding*(j+1),sum(maxHeights[:i])*size+padding*(i+1))
        s = r"""
            <canvas id='drawing_on_cell_%s'>
            Your browser does not support this awesome feature. You should probably go download firefox 3+ now. notruncate !
            </canvas>
            <SCRIPT type="text/javascript">
            var cellID = %s;
            var P = %s;
            var padding = %s;
            var SQUARE_SIZE = %s;
            var BORDER_WIDTH = %s;
            var maxHeights = %s;
            var maxHeightsSum = %s;
            var boxMaxWidth = %s;
            var InnerBorder = %s;
            var OuterBorder = %s;
            var boxBorder = %s;
            loaded = function(){
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                drawingBox.setAttribute('width',boxMaxWidth);
                drawingBox.setAttribute('height',maxHeightsSum*SQUARE_SIZE+padding*(maxHeights.length+1));
                drawingBox.style.border = boxBorder+'px solid black';
            }
            drawSquares = function(){
                %s
            }
            setTimeout(loaded, 200);
            setTimeout(drawSquares, 600); 
            </SCRIPT>"""%(cellID,cellID,self.set,padding,size,borderWidth,maxHeights,sum(maxHeights),boxWidth,innerBorder,outerBorder,boxBorder,innerDrawingJS)
        return html(s)
