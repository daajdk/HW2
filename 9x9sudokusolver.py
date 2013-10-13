#!/usr/bin/env python
# DAA HW2
# Mini Sudoku Brute Force Solver with backtracking
# Python version
# Kevin McCarthy, Jen Senior, Dan Wegmann
# 12 Oct 2013
# Prof. Baliga

#sys module imported for parsing input file from args
#time module imported for runtime analysis
import sys
import time
import copy

#class EmptyCell used to store cell info such as 
#coordinates and all possible solutions as attributes
class EmptyCell:
    def __init__(self, row, col):
        self.coord = [row, col]
        self.boxAvail = []
        self.rowAvail = []
        self.colAvail = []
        self.possSol = []
        self.row = row
        self.col = col
        self.box = 0
        
    #get possible solutions for cell row and store     
    def getRowNums(self, obj, Puzzle):
        row = self.coord[0]
        a = []
        for i in range(0,obj.size):
            a.append(Puzzle[row][i])
        for i in range(1,obj.size+1):
             if i not in a:
                self.rowAvail.append(i)
    
    #get possible solutions for cell column and store        
    def getColNums(self, obj, Puzzle):
        col = self.coord[1]
        a = []
        for i in range(0,obj.size):
            a.append(Puzzle[i][col])
        for i in range(1,obj.size+1):
             if i not in a:
                self.colAvail.append(i)
    
    #get possible solutions for cell box and store
    def getBoxNums(self, obj, Puzzle):
        row = 0
        col = 0
        a = []
        if obj.size == 6:
            if(self.coord[0] <= 1):
                if(self.coord[1] <= 2):
                    row = 0
                    col = 0
                    self.box = 1
                else:
                    row = 0
                    col = 3
                    self.box = 2
            elif(self.coord[0] <= 3):
                if(self.coord[1] <= 2):
                    row = 2
                    col = 0
                    self.box = 3
                else:
                    row = 2
                    col = 3
                    self.box = 4
            elif(self.coord[0] <= 5):
                if(self.coord[1] <= 2):
                    row = 4
                    col = 0
                    self.box = 5
                else:
                    row = 4
                    col = 3
                    self.box = 6
            for i in range(row,row+2):
                for j in range(col, col+3):
                    a.append(Puzzle[i][j])
        if obj.size == 9:
            if self.coord[0] <= 2:
                if self.coord[1] <= 2:
                    row = 0
                    col = 0
                    self.box = 1
                elif (self.coord[1] > 2 and self.coord[1] <= 5):
                    row = 0
                    col = 3
                    self.box = 2
                elif (self.coord[1] > 5 and self.coord[1] <= 8):
                    row = 0
                    col = 6
                    self.box = 3
            elif (self.coord[0] > 2 and self.coord[0] <= 5):
                if self.coord[1] <= 2:
                    row = 3
                    col = 0
                    self.box = 4
                elif (self.coord[1] > 2 and self.coord[1] <= 5):
                    row = 3
                    col = 3
                    self.box = 5
                elif (self.coord[1] > 5 and self.coord[1] <= 8):
                    row = 3
                    col = 6
                    self.box = 6
            elif (self.coord[0] > 5 and self.coord[0] <= 8):
                if self.coord[1] <=2:
                    row = 6
                    col = 0
                    self.box = 7
                elif (self.coord[1] > 2 and self.coord[1] <= 5):
                    row = 6
                    col = 3
                    self.box = 8
                elif (self.coord[1] > 5 and self.coord[1] <= 8):
                    row = 6
                    col = 6
                    self.box = 9
            for i in range(row,row+3):
                for j in range(col, col+3):
                    a.append(Puzzle[i][j])
        for i in range(1,obj.size+1):
            if i not in a:
                self.boxAvail.append(i)
        
    #get possible solutions for cell after taking into account
    #row, cell, and box possible solutions; store as attribute    
    def availCell(self, obj):
        box = self.boxAvail
        row = self.rowAvail
        col = self.colAvail
        for i in range(1,obj.size+1):
            if i in box and row and col:
                self.possSol.append(i)
    
    #check row of puzzle for equal number
    def inRow(self, row, val, Puzzle, obj):
        if val in Puzzle[row]:
            return True
        else:
            return False
            
    #check col of puzzle for equal number
    def inCol(self, col, val, Puzzle, obj):
        for i in range(0,obj.size):
            if(Puzzle[i][col]==val):
                return True
        return False
    
    #check cell box of puzzle for equal number
    def inBox(self, box, val, Puzzle, obj):
        boxRow = 0
        boxCol = 0
        if (obj.size == 6):
            if box == 2:
                boxRow = 0
                boxCol = 3
            if box == 3:
                boxRow = 2
                boxCol = 0
            if box == 4:
                boxRow = 2
                boxCol = 3
            if box == 5:
                boxRow = 4
                boxCol = 0
            if box == 6:
                boxRow = 4
                boxCol = 3
            for i in range(boxRow,boxRow+2):
                for j in range(boxCol, boxCol+3):
                    if(Puzzle[i][j] == val):
                        return True
            return False
        elif (obj.size == 9):
            if box == 2:
                boxRow = 0
                boxCol = 3
            if box == 3:
                boxRow = 0
                boxCol = 6
            if box == 4:
                boxRow = 3
                boxCol = 0
            if box == 5:
                boxRow = 3
                boxCol = 3
            if box == 6:
                boxRow = 3
                boxCol = 6
            if box == 7:
                boxRow = 6
                boxCol = 0
            if box == 8:
                boxRow = 6
                boxCol = 3
            if box == 9:
                boxRow = 6
                boxCol = 6
            for i in range(boxRow,boxRow+3):
                for j in range(boxCol, boxCol+3):
                    if(Puzzle[i][j] == val):
                        return True
            return False
            

#MiniSudoku class to contain functions related to solving the Mini Sudoku puzzle
class Sudoku:
    def __init__(self):
        self.size = 0
        self.solvedPuzzle = []
        self.isSolved = False
    
    #checks to see if the row has all 6 proper digits
    #vars set to false until it's corresponding digit 
    #is found in the row passed as arg                     
    def checkRow(self, row, Puzzle):
        a = []
        for i in range(0,self.size):
            a.append(Puzzle[row][i])
        for i in range(1,self.size+1):
            if i not in a:
                return False
        return True 

    #checks to see if the column has all 6 proper digits
    #same concept as checkRow in with obvious difference
    def checkCol(self, col, Puzzle):
        a = []
        for i in range(0,self.size):
            a.append(Puzzle[i][col])
        for i in range(1,self.size+1):
            if i not in a:
                return False
        return True    
    
    #do final check on puzzle to see if solved yet
    def finalCheck(self, Puzzle):
        rowStatus = True
        colStatus = True
        for i in range(0,self.size):
            rowStatus = self.checkRow(i,Puzzle)
            colStatus = self.checkCol(i,Puzzle)
            if(not rowStatus or not colStatus):
                return False
        if((rowStatus) and (colStatus)):
            return True
        else:
            return False        
    
    #build the unsolved puzzle matrix from the given input
    def buildPuzzle(self, f):
        a = []
        row = 0
        col = 0
        for j in f:
            for i in j:
                if i == '\n':
                    pass
                else:    
                    self.size+=1
            if(self.size%6==0 and self.size%9==0):
                self.size = 6
            elif(self.size%9==0 and self.size%6==3):   
                self.size = 9
            for t in range(1,self.size+1):
                a.append([])    
            for i in j:
                if (col % self.size == 0 and col > 0):
                    col = 0
                    row+=1
                if (i != "\n"):
                    a[row].append(int(i))
                    col+=1
            break
        return a
    
    #build the set of EmptyCells objects and return it
    def buildEmptyCells(self, obj, Puzzle):
        a = []
        for i in range(0,obj.size):
            for j in range(0,obj.size):
                if(Puzzle[i][j]==0):
                    ec = EmptyCell(i,j)
                    a.append(ec)
        return a
    
    #get file descriptor for input, and open in append mode
    #to leave initial unsolved puzzle data in file after solving
    def getFile(self):
        data = sys.argv[1]
        return open(data, 'a+')
    
    #append solution output to input file
    def writeToFile(self, f, Puzzle, end_time):
        if(self.isSolved):
            f.write("\n***********SOLUTION***********\n")
            for i in Puzzle:
                for j in i:
                    f.write(str(j))
            f.write("\nTotal Runtime in seconds: "+str(end_time))
        f.close()
    
    #function to begin solving the puzzle which is the root of the
    #recursive call tree
    def solve(self):
        start_time = time.time()
        f = self.getFile()
        obj = self
        Puzzle = self.buildPuzzle(f)
        EmptyCells = self.buildEmptyCells(obj, Puzzle)
        for i in EmptyCells:
            i.getRowNums(obj, Puzzle)
            i.getColNums(obj, Puzzle)
            i.getBoxNums(obj, Puzzle)
            i.availCell(obj)
        self.reck(EmptyCells, 0, obj, Puzzle)
        end_time = time.time()-start_time
        if(self.isSolved):
            print "\n***************\nSuccess!!!\n",self.solvedPuzzle,"\n***************"
            print"\nTotal Runtime in seconds: ", end_time
            self.writeToFile(f, self.solvedPuzzle, end_time)
        else:
            print"NOT SOLVED!"
    
    #recursive function which uses copies of the puzzle passed to it as the
    #backtracking method
    def reck(self, EmptyCells, placer, obj, Puzzle):
        index = placer
        for i in EmptyCells[index].possSol:
            a = copy.deepcopy(Puzzle)
            if(not obj.isSolved):
                if not EmptyCells[index].inRow(EmptyCells[index].row, i, a, obj) and not EmptyCells[index].inCol(EmptyCells[index].col, i, a, obj) and not EmptyCells[index].inBox(EmptyCells[index].box, i, a, obj):
                    a[EmptyCells[index].coord[0]][EmptyCells[index].coord[1]] = i
                    if(self.finalCheck(a)):
                        obj.isSolved = True
                        obj.solvedPuzzle = copy.deepcopy(a)
                        return
                    elif(index < len(EmptyCells)-1 and not obj.isSolved):
                        self.reck(EmptyCells,index+1,obj, a)
        
def main():
    test = Sudoku()
    test.solve()
       
if __name__ == "__main__":
    main()
