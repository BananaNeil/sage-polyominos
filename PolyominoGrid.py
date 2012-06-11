PolyominoColorDictStr = ["■","□","◪","◩","▧","▣","▥","▤","▢","#","+","O","X"]
PolyominoColorDict = {}
class PolyominoGrid:
    def __init__(self,grid=None,h=0,w=0):
        self.pieceCount = 0 if grid is None else 1
        if type(grid)==list:
            self.grid = grid
            self.binaryGrid = [[(1 if grid[h][w]!=0 else 0) for w in range(len(grid[0]))] for h in range(len(grid))]
        else:
            self.grid = copy(grid)._p
            self.binaryGrid = [[(1 if self.grid[h][w]!=0 else 0) for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        if self.grid is None or self.grid==[]:
            self.grid = [[0 for i in range(w)] for j in range(h)]
            self.binaryGrid = [[0 for i in range(w)] for j in range(h)]
            if h==0 and w==0:
                self.width = 0
                self.height = 0
        else:
            self.width = len(self.grid[0])
            self.height = len(self.grid)
        
    def __len__(self): ##
        return self.pieceCount
            
    def __eq__(self,other):
        if not (self.width==other.width and self.height==other.height):
            return False
        for h in range(len(self.grid)):
            for w in range(len(self.grid[0])):
                if not ((self.grid[h][w]==other.grid[h][w] and self.grid[h][w]==0) or (other.grid[h][w]!=0 and self.grid[h][w]!=0)):
                    return False
        return True
        
    def __ne__(self,other):
        return not self==other
        
    def __hash__(self):
        return hash(self.binaryStr())
        
    def __str__(self):
        string = ""
        for h in range(len(self.grid)):
            string += "\n"
            for w in range(len(self.grid[0])):
                string += PolyominoColorDictStr[self[h][w]-1] if self[h][w]!=0 else " "
                string += " "
        return string 
        
    def __repr__(self):
        return str(self.grid)
        
    def __copy__(self): ##
        newPG = PolyominoGrid(grid=[[self.grid[h][w] for w in range(len(self.grid[0]))] for h in range(len(self.grid))])
        newPG.pieceCount = self.pieceCount
        return newPG
        
    def __getitem__(self,n):
        return self.grid[n]
    
    def binaryStr(self): 
        return "\n".join(str(x) for x in self.binaryGrid)
        
    def _isConnected(self,h,w):
        return ((h+1<len(self.grid) and  not self.grid[h+1][w]==0) or (w+1<len(self.grid[0]) and not self.grid[h][w+1]==0) or (w-1>=0 and not self.grid[h][w-1]==0) or (h-1>=0 and not self.grid[h-1][w]==0))
        
    def openSpaces(self,expand=true):
        newP = copy(self)
        if expand:
            newP.insertRows(index=0)
            newP.insertRows()
            newP.insertColumns(index=0)
            newP.insertColumns()
            return [[h-1,w-1] for w in range(newP.width) for h in range(newP.height) if newP[h][w]==0 and newP._isConnected(h,w)]
        return [[h,w] for w in range(newP.width) for h in range(newP.height) if newP[h][w]==0 and newP._isConnected(h,w)]
    
    def insertColumns(self,numOfColumns=1,index=None): 
        if index is None:
            index = self.width
        for i in range(numOfColumns):
            for h in self.grid:
                h.insert(index,0)
            for h in self.binaryGrid:
                h.insert(index,0)
            self.width += 1
   
    def insertRows(self,numOfRows=1,index=None): 
        if index is None:
            index = self.height
        for i in range(numOfRows):
            self.grid.insert(index,[0 for w in range(self.width)])
            self.binaryGrid.insert(index,[0 for w in range(self.width)])
            self.height += 1
    
    def removeColumns(self,numOfColumns=1,index=None):
        if index is None:
            index = self.width
        if numOfColumns>0:
            for h in self.grid:
                h = h[:index] + h[(index+numOfColumns):]
                self.height -= numOfColumns
            for h in self.binaryGrid:
                h = h[:index] + h[(index+numOfColumns):]
    
    def removeRows(self,numOfRows=1,index=None):
        if index is None:
            index = self.height
        if numOfRows>0:
            self.grid = self.grid[:index] + self.grid[index+numOfRows:]
            self.binaryGrid = self.binaryGrid[:index] + self.binaryGrid[index+numOfRows:]
            self.height -= numOfRows
            
    def isSymmetricR(self):
        bg = copy(self.binaryGrid)
        return self.binaryGrid == [a[::-1] for a in bg][::-1]
            
    def addPiece(self,P,h_p=0,w_p=0,h_g=0,w_g=0):
        self.pieceCount += 1
        if self.grid == []:
            self.grid = copy(P)._p
            self.height = P.getHeight()
            self.width = P.getWidth()
        else:
            w = w_g-w_p
            h = h_g-h_p
            wontFit = false
            for H in range(P.getHeight()):
                for W in range(P.getWidth()):
                    if (H+h>=0) and (W+w>=0) and (H+h<self.height) and (W+w<self.width):
                        if self.grid[H+h][W+w]!=0 and P[H][W]!=0:
                        #if self.grid[H+(h if h>0 else 0)][W+(w if w>0 else 0)]!=0 and P[H][W]!=0:
                            wontFit = true
            if wontFit:
                self.pieceCount -= 1
                return None
            P = copy(P)
            originalGrid = [copy(i) for i in self.grid]
            self.insertColumns(-w,0)
            self.insertColumns(P.getWidth()-self.width+(w if w>0 else 0))
            self.insertRows(-h,0)
            self.insertRows(P.getHeight()-self.height+(h if h>0 else 0))
            for H in range(P.getHeight()):
                for W in range(P.getWidth()):
                    if P[H][W]!=0:
                        self.grid[H+(h if h>0 else 0)][W+(w if w>0 else 0)] = self.pieceCount
                        self.binaryGrid[H+(h if h>0 else 0)][W+(w if w>0 else 0)] = 1
            return self
        
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
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                var context = drawingBox.getContext('2d');
                //document.getElementById('drawing_on_cell_'+cellID).innerHTML = P;
                for (h=0;h<height;h++){
                    for (w=0;w<width;w++){
                    
                        context.fillStyle = "rgb(0,0,255)";
                        context.lineWidth = BORDER_WIDTH;
                        context.strokeStyle = "rgb(0,0,0)";
                        if (P[h][w]!=0){                        
                            context.fillRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, SQUARE_SIZE);
                            if(InnerBorder==1){
                                context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, SQUARE_SIZE);
                            } else if (OuterBorder==1){
                                //left
                                if (w==0 || P[h][w-1]!=P[h][w]){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), 0, SQUARE_SIZE);
                                }
                                //right
                                if (w==width-1 || P[h][w+1]!=P[h][w]){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*(w+1)), yPos+((SQUARE_SIZE)*h), 0, SQUARE_SIZE);
                                }
                                //top
                                if (h==0 || P[h-1][w]!=P[h][w]){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*h), SQUARE_SIZE, 0);
                                }
                                //bottom
                                if (h==height-1 || P[h+1][w]!=P[h][w]){
                                    context.strokeRect(xPos+((SQUARE_SIZE)*w), yPos+((SQUARE_SIZE)*(h+1)), SQUARE_SIZE, 0);
                                }
                            }
                        }
                    }
                }
        """%(cellID,self.grid,self.height,self.width,size,border_width,xPos,yPos)
        
    def draw(self,other=None,size=35,borderWidth=None,padding=20,innerBorder=false,outerBorder=true,cellID=None,boxBorder=2):
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
        boxWidth = 2*padding+size*self.width
        if not other is None:
            boxWidth += padding+other.width*size
            innerDrawingJS += other.generateDrawingJS(cellID,size,borderWidth,2*padding+size*self.width,padding)
        s = r"""
            <canvas id='drawing_on_cell_%s'>
            Your browser does not support this awesome feature. You should probably go download firefox 3+ now. notruncate
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
            var boxBorder = %s;
            var boxWidth = %s;
            loaded = function(){
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                var drawingBox = document.getElementById('drawing_on_cell_'+cellID);
                drawingBox.setAttribute('width',boxWidth);
                drawingBox.setAttribute('height',2*padding+SQUARE_SIZE*(height));
                drawingBox.style.border=boxBorder+'px solid black';
            }
            drawSquares = function(){
                %s
            }
            setTimeout(loaded, 200);
            setTimeout(drawSquares, 600); 
            </SCRIPT>"""%(cellID,cellID,self.grid,padding,size,borderWidth,self.height,self.width,innerBorder,outerBorder,boxBorder,boxWidth,innerDrawingJS)
        return html(s)
