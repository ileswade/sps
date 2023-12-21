class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class rangeType:
    ROW = 1
    COLUMN = 2
    BOX = 4
    KING = 8
    KNIGHT = 16

class rules:
    basic = rangeType.ROW | rangeType.COLUMN | rangeType.BOX
    knight = rangeType.ROW | rangeType.COLUMN | rangeType.BOX | rangeType.KNIGHT
    king = rangeType.ROW | rangeType.COLUMN | rangeType.BOX | rangeType.KING

org=[]
boardx=[]
gameRules = 0
thisGame=5
Boards=[]
Boards.append((rules.knight,"--36-81-- -4-----7- 2-------3 6---9---8 ---1-2--- 7---6---4 4-------1 -6-----2- --54-98--")) # 0 -
Boards.append((rules.basic, "-6-3--8-4 537-9---- -4---63-7 -9--51238 --------- 71362--4- 3-64---1- ----6-523 1-2--9-8-")) # 1 -
Boards.append((rules.knight,"--59632-- --------- 2---8---9 7-------2 5-8---9-6 3-------4 8---5---7 --------- --76984--")) # 2 -
Boards.append((rules.basic, "-72--9--- -3-6--4-- --1----87 1-----7-- 9--2-3--- --------6 ---3--56- -----49-- ----18--2")) # 3 - https://www.youtube.com/watch?v=-24S4mHY73w
Boards.append((rules.basic, "8----63-5 -4-----7- --------- -1--387-4 ---1-4--- 3---7-29- -----3--- -2-----4- 5-68----2")) # 4 - https://www.youtube.com/watch?v=pWqUzSgJCE0
Boards.append((rules.king , "17-8-3--6 --3-----8 ---2---3- 5-----6-2 ----2---- 3-9-----1 -8---7--- 6-----3-- 7--5-2-19")) # King # 10 iPad



def displayBoard(board, HighLightSet=None):
    print("+-------+-------+-------+")
    for r in range(0, 9):
        thisRow = "| "
        for c in range(0, 9):
            accent=""
            o_val = org[r][c]
            c_val = board[r][c]
            
            p_val=str(c_val)
            
            if c_val==o_val:
                accent=color.GREEN
            if HighLightSet is not None:
                for eachItem in HighLightSet:
                    if eachItem[0]==r and eachItem[1]==c:
                        accent=color.YELLOW
            if  isinstance(c_val, list): p_val="-"
            if accent!="":
                p_val=accent+p_val+color.END
            thisRow+=p_val+" "
            if (c+1) % 3 == 0: thisRow+="| "
        print(thisRow)
        if (r+1) % 3 == 0: print("+-------+-------+-------+")

def displayBoardPencils(board):
    for row in range(0,9):
        for column in range(0,9):
            value=board[row][column]
            if isinstance(value, list):
                print("({}, {}) is {}".format(row,column,value))

def place(board, row, column, value, note, debug):
    if isinstance(org[row][column], list):  # this prevents overwritting the original value
        board[row][column]=value
        if isinstance(org[row][column], list)==False:
            if note=="":
                if debug: print("Placed {} at {}, {}.".format(value, row, column))
            else:
                if debug: print("Placed {} at {}, {} determine by {}.".format(value, row, column, note))

def getRange(board, requestedRange, row, column, includeMe=True): # requestedRange is the currently being used ruleset
    returnData = []
    workingData =[]
    if requestedRange & rangeType.ROW:
        for columnCounter in range(0,9):
            workingData.append((row,columnCounter))
    if requestedRange & rangeType.COLUMN:
        for rowCounter in range(0,9):
            workingData.append((rowCounter,column))
    if requestedRange & rangeType.BOX:
        rowStart = 3*int(row/3)
        columnStart = 3*int(column/3)
        for rowCounter in range(rowStart,rowStart+3):
            for columnCounter in range(columnStart,columnStart+3):
                workingData.append((rowCounter,columnCounter))
    if requestedRange & rangeType.KING:
        for rowCounter in range (row-1,row+2):
            for columnCounter in range(column-1, column+2):
                if rowCounter>=0 and rowCounter<=8 and columnCounter>=0 and columnCounter<=8:
                    workingData.append((rowCounter,columnCounter))
    if requestedRange & rangeType.KNIGHT:
        references = [(-1,-2),(-2,-1),(-2, 1),(-1,2),(0,0),(1,2),(2,1),(2,-1),(1,-2)]
        for eachReference in references:
            deltaX = row + eachReference[0]
            deltaY = column + eachReference[1]
            if deltaX>=0 and deltaX<=8 and deltaY>=0 and deltaY<=8:
                workingData.append((deltaX,deltaY))
    if includeMe==False:
        workingData.remove((row, column))
    for eachCell in workingData:
        newValue=(eachCell[0], eachCell[1],board[eachCell[0]][eachCell[1]])
        if newValue not in returnData:
            returnData.append(newValue)
    return returnData

def getValues(rangeSet):
    penMarks=[]
    pencilMarks=[]
    for row, columnm, cellContents in rangeSet:
        if isinstance(cellContents, list): #true=Pencil, false=pen
            for eachPencil in cellContents:
                if eachPencil not in pencilMarks:
                    pencilMarks.append(eachPencil)
        else:
            if cellContents not in penMarks:
                penMarks.append(cellContents)
    penMarks.sort()
    pencilMarks.sort()
    return((penMarks, pencilMarks))

def checkCell(board, currentRules, row, column, debug):
    if isinstance(board[row][column],list):  # We only assess a cell if it has pencilmarks on it currently
        collectiveRange = getRange(board, currentRules, row, column, False)  # get all the cells influencing this cell (excluding this cell) using the currentRule set
        collectiveValues = getValues(collectiveRange)
        penMarksNotPresent = setInverse(collectiveValues[0])
        if len(penMarksNotPresent)==1:  # If there is only one missing Penmark, then that value has to be this cells solution
            place(board,row,column,penMarksNotPresent[0],"absent PenMark",debug) # so set the penMark as the solution
            return True
        if scanPencils(board, row, column, debug):
            return True
        place(board, row,column,penMarksNotPresent,"",debug) # place the revised PencilMarks (which is the PenMakrs not present)

def scanPencils(board, row,column,debug):
    rRange = getRange(board, rangeType.ROW, row, column, False)
    cRange = getRange(board, rangeType.COLUMN, row, column, False)
    bRange = getRange(board, rangeType.BOX,row, column, False)

    rValues = getValues(rRange)
    cValues = getValues(cRange)
    bValues = getValues(bRange)

    rValues = setInverse(setUnion(rValues[0],rValues[1]))
    cValues = setInverse(setUnion(cValues[0],cValues[1]))
    bValues = setInverse(setUnion(bValues[0],bValues[1]))
    if len(rValues)==1:
        place(board, row, column, rValues[0],"unique pencil in row", debug)
        return True
    if len(cValues)==1:
        place(board, row, column, cValues[0],"unique pencil in column", debug)
        return True
    if len(bValues)==1:
        place(board, row, column, bValues[0],"unique pencil in box", debug)
        return True  

def checkBoard(board, currentRules, debug=False):
    flag=True
    c=0
    while flag:
        flag=False
        c+=1
        if debug: print("Interation {}".format(c))
        for row in range(0,9):
            for column in range(0,9):
                if checkCell(board,currentRules, row, column,debug):
                    flag=True
        if debug: displayBoard(board)

def setIntersect(setA, setB):
    returnData = []
    for eachItem in setA:
        if eachItem in setB:
            returnData.append(eachItem)
    return returnData

def setUnion(setA, setB):
    returnData = list(setA)
    for eachItem in setB:
        if eachItem not in returnData:
            returnData.append(eachItem)
    return returnData

def setInverse(setA):
    returnData = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    dataSet = list(setA)
    if len(dataSet):
        if isinstance(setA[0],tuple) == True:
            dataSet = setGetFromBoard(setA)
    for eachItem in dataSet:   
        if  isinstance(eachItem, list) == False:
            if eachItem in returnData:
                returnData.remove(eachItem)
    return returnData

def updateBoard():
    # Look at all values within range and see if "only one" value is missing.  If it is, then that value needs to be here
    flag=True
    while flag==True:
        flag=False
        for r in range(0,9):
            for c in range(0,9):
                flag=updateCell(r,c)



    # Scan all the pencil makes in a single range.  If a pencil value exists in one (and only one cell) and does not exist in the single range in general, then that value must be here

                
def parseBoard(boardSetup):
    returnData=[]
    rows=boardSetup.split()
    for eachRow in rows:
        row=[]
        for i in range(0,9):
            cha=eachRow[i]
            if cha<"1" or cha>"9":
                row.append([1,2,3,4,5,6,7,8,9])
            else:
                row.append(int(cha))
        returnData.append(row)
    return returnData
    
def initalizeBoard(id):
    global org
    global boardx
    global gameRules
    thisGameRules=Boards[id][0]
    thisGameSetup=Boards[id][1]
    parsedBoard=parseBoard(thisGameSetup)
    org=parsedBoard.copy()
    boardx=parsedBoard.copy()
    gameRules = thisGameRules

initalizeBoard(thisGame)
place(boardx,6,3,4,"forced guess",False)
place(boardx,4,1,6,"forced guess",False)

displayBoard(boardx)
checkBoard(boardx, gameRules)
displayBoardPencils(boardx)
displayBoard(boardx)


#updateBoard()
#scanPencils(setType.COLUMN,0,0)  