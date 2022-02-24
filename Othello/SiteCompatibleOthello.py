# Name: Tommy Williams 
# Date: 1/18/2022

import copy
import random


class Strategy:

   def __init__(self):
      self.white = "o"
      self.black = "x"
      self.directions = [-9, -1, 7, -8, 8, -7, 1, 9]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 8
      self.y_max = 8
      self.logging = True
      self.weightedBoard = [25,-10,5,7,7,5,-10,25,
                            -10,-8,-1,-1,-1,-1,-12,-10,
                            5,-1,1,0,0,1,-1,5,
                            7,-1,0,1,1,0,-1,7,
                            7,-1,0,1,1,0,-1,7,
                            5,-1,1,0,0,1,-1,5,
                            -10,-12,-1,-1,-1,-1,-12,-10,
                            25,-10,5,7,7,5,-10,25]

      
   def best_strategy(self, board, color,best_move,still_running,time_limit):
      if color == "#000000" or color == "x":
         color = "x"
      else:
         color = "o"
      
      depth=2
      print("Eval at Depth 0:" + str(self.placementValue(board,color)))
      while still_running:
         e, best_move.value = self.alphabeta(board,color,depth,-9999,9999,True)
         #e,best_move.value = self.minimax(board,color,0,depth)
         depth+=1
         if depth==4:
            print("eval at Depth 4:",e,best_move.value)
         if depth==5:
            print("Eval at Depth 5:",e,best_move.value)
         if depth==6:
            print("Eval at Depth 6:",e,best_move.value)
         if depth>=7 and depth<=10:
            print("Eval at Depth",depth,e)
            
      return best_move.value

   def evalu(self, board, color, maxDepth):
      board = board.replace('*','.')
      i=0
      while i<64:
         print(board[i:i+8])
         i+=8
      print("Eval at Depth 0:" + str(self.placementValue(board,color)))
      depth = 1
      while depth<=maxDepth:
         e,best_move = self.alphabeta(board,color,depth,-9999,9999,True)
         print("Eval at Depth %d" % (depth), e)
         print("Best move is", best_move)
         print()
         depth+=1

   def getChildren(self, board, color):
      children = []
      for s in self.find_moves(board,color):
          children.append((self.make_move(board,color,s),s[0]))
      return children

   def minimax(self, board, color, prevMove, search_depth):
      moves = self.find_moves(board,color)
      if search_depth == 0 or len(moves)==0:
         return self.evaluate(board,self.opposite_color[color]),[]  #add in find_moves later
      v = -999
      for s in moves:
         tempState = self.make_move(board,color,s)
         w,tr = self.minimax(tempState,self.opposite_color[color],s,search_depth-1)
         w = -1*w
         if w>v:
            best_move = s[0]
            v = w
      return v, best_move

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1

   def placementValue(self,board,color):
      evalY, evalN, totalY, totalN = 0, 0, 0, 0
      for z in range(len(board)):
         if board[z] == color:
            evalY += self.weightedBoard[z]
            totalY += 1
         elif board[z] == self.opposite_color[color]:
            evalN += self.weightedBoard[z]
            totalN += 1
      if totalN==0: return 9999
      elif totalY==0: return -9999
      return evalY-evalN
      
   def alphabeta(self, board, color, depth, alpha, beta, maximizing):
      if depth == 0 or self.stones_left(board)==0:
         if self.stones_left(board)>10:   
            return self.evaluate(board,color),0
         else:
            return self.terminalEval(board,color),0
      if maximizing:
          v = -9999
          move = 0
          children = self.getChildren(board,color)
          if len(children)==0:
             if len(self.getChildren(board,self.opposite_color[color]))!=0:
                return self.alphabeta(board,color,depth,alpha,beta,False)[0]-100,0
             else:
                if self.num_pieces(board,color)>0: return 9999,0
                else: return -9999,0
          #children = [j for i,j in sorted([(self.placementValue(child[0],color),child) for child in children])]
          for child,pos in children:
             ev = self.alphabeta(child,color,depth-1,alpha,beta,False)[0]
             if ev>v:
                move = pos
                v = ev
             alpha = max(alpha,v)
             if v >= beta:
                break
          return v,move
      else:
          other = self.opposite_color[color]
          move = 0
          v = 9999
          children = self.getChildren(board,self.opposite_color[color])
          if len(children)==0:
             if len(self.getChildren(board,color))!=0:
                return self.alphabeta(board,color,depth,alpha,beta,True)[0]+100,0
             else:
                if self.num_pieces(board,color)>0: return 9999,0
                else: return -9999,0
          #children = [j for i,j in sorted([(self.placementValue(child[0],other),child) for child in children])]
          for child,pos in children:
              ev = self.alphabeta(child,color,depth-1,alpha,beta,True)[0]
              #if pos in (0,7,56,63): print(ev)
              if ev<v:
                 move = pos
                 v = ev
              beta = min(beta,v)
              if v <= alpha:
                 break
          return v,move

   def make_key(self, board, color):
    # hashes the board
      return 1

   def make_move(self, board, color, move):
      s = self.flipPieces(board,move[1],color)
      return s[:move[0]]+color+s[move[0]+1:]

   def manuevarability(self,board,color,possible_moves,opp_moves):
      return len(possible_moves)-len(opp_moves)

   def stableCheck(self,board,z,color,direction,stables):
      #use self.directions
      stability = {}
      for d in self.directions:
         stability[d] = False
      stability[direction] = True
      stability[-1*direction] = True
      for pos in self.getAdjacents(z):
         d = pos-z
         while stability[d]==False: 
            if board[pos]==color:
               if pos in stables or (pos+d<0 or pos+d>63 or abs((pos+d)%8-pos%8)>1):
                  stability[d] = True
                  stability[-1*d] = True
                  break
            elif board[pos]=='.':
               stability[d] = False
               break
            else:
               stability[d] = False
               break
            pos+=d
      return not False in stability.values()

   def recursiveStability(self,board,z,color,direction,stables):
      if z in stables or self.stableCheck(board,z,color,direction,stables):
         stables.append(z)
         for pos in self.getAdjacents(z):
            d = pos-z
            if board[pos]==color and not pos in stables:
               return self.recursiveStability(board,pos,color,d,stables)
      return list(set(stables))

   def stability(self,board,color):
      stableCount = 0
      stables = []
      for z in (0,7,56,63):
         if board[z] == color:
            stables.append(z)
      z=0
      while (z<len(stables)):
         stables = self.recursiveStability(board,stables[z],color,0,stables)
         z+=1
      return len(stables)*2

   def capturability(self,board,color,revFlipped):
      nonCapturable = 0
      rSetFlipped = set()
      for z in revFlipped:
         rSetFlipped = rSetFlipped.union(set(z))
      for z in range(len(board)): 
         if board[z] == color:
            if not z in rSetFlipped:
               nonCapturable+=1
            else:
               nonCapturable-=1
      return nonCapturable

   def evaluate(self, board, color):
      evaluation = 0
      playerMoves = self.find_moves(board,color)
      possible_flipped = [j for i,j in playerMoves]
      possible_moves = [i for i,j in playerMoves]
      otherMoves = self.find_moves(board,self.opposite_color[color])
      opp_flipped = [j for i,j in otherMoves]
      opp_moves = [i for i,j in otherMoves]

      if len(possible_moves) == 0 and len(opp_moves) == 0:
         if  self.num_pieces(board,color)>0:
            return 9999
         else:
            -9999
      elif len(possible_moves) == 0:
         evaluation-=10
      elif len(opp_moves) == 0:
         evaluation+=60
      
      p = self.placementValue(board,color)
      m = self.manuevarability(board,color,possible_moves,opp_moves)
      #s = self.stability(board,color)-self.stability(board,self.opposite_color[color])
      d = self.capturability(board,color,opp_flipped)-self.capturability(board,self.opposite_color[color],possible_flipped)
      c = 0
      for corner in (0,7,56,63):
         if corner in possible_moves or board[corner] == color: c+=20
         elif corner in opp_moves or board[corner] == self.opposite_color[color]: c-=20
      if self.stones_left(board)>32:
         evaluation = p+c+m+d
      else:
         s = self.stability(board,color)-self.stability(board,self.opposite_color[color])
         evaluation  = p+s*2+c+d/2
      return evaluation
      #return p+s*2+c+d/2+m
      #return self.placementValue(board,color)

   def terminalEval(self,board,color):
      playerMoves = self.find_moves(board,color)
      possible_flipped = [j for i,j in playerMoves]
      otherMoves = self.find_moves(board,self.opposite_color[color])
      opp_flipped = [j for i,j in otherMoves]

      d = self.capturability(board,color,opp_flipped)-self.capturability(board,self.opposite_color[color],possible_flipped)
      t = self.num_pieces(board,color)
      p = self.placementValue(board,color)

      return d+p*2+t
      
      
   def num_pieces(self,board,color):
      count = 0
      for z in board:
         if z == color:
            count+=1
         elif z == self.opposite_color[color]:
            count-=1
      return count

   def score(self, board, color):
      blackScore,whiteScore = 0,0
      for pos in board:
         if pos=='x':
            blackScore+=1
         elif pos=='o':
            whiteScore+=1
      return 1

   def stones_left(self, board):
      count = 0
      for pos in board:
            if pos=='.':
               count+=1
      return count

   def flipPieces(self,board,pieces,color):
      prev = 0
      newPos = ""
      for p in sorted(list(set(pieces))):
         newPos+=board[prev:p]+color
         prev = p+1
      newPos+=board[prev:]
      if len(newPos)!=64:
         print(board)
         print(newPos)
         print(set(sorted(pieces)))
         raise SyntaxError
      return newPos

   def getAdjacents(self, index):
      moves = ()
      s,e = 0,8
      if index%8==0: s = 3
      elif index%8==7: e = 5
      for i in range(s,e):
         posChange = self.directions[i]
         if index+posChange>=0 and index+posChange<64:
            moves+=(index+posChange,)
      return moves
   
   def find_moves(self, board, color):
      moves = []
      for z in range(len(board)):
         if board[z]=='.':
            for pos in self.getAdjacents(z):
               if board[pos] == self.opposite_color[color]:
                  flip = self.find_flipped(board,z,color)
                  if len(flip)>0:
                      moves.append((flip[-1],flip[:-1]))
      return moves

   def captureChecker(self,board,z,pos,color):
      flipped = ()
      delta = pos-z
      if pos<0 or pos>63 or abs(pos%8-z%8)>1: return False
      if board[pos] == self.opposite_color[color]:
          recur = self.captureChecker(board,pos,pos+delta,color)
          if recur==False: return False
          else: return recur+(z,)
      elif board[pos] == color:
          return (z,)
      else:
         return False
      
   def find_flipped(self, board, z, color):
      flipped = ()
      for pos in self.getAdjacents(z):
         if board[pos]==self.opposite_color[color]:
            recur = self.captureChecker(board,z,pos,color)
            if recur != False: flipped += recur
      return flipped

"""
s = Strategy()
s.evalu("xxxxxxx*xooooxx*xooxxxxxxxooxxxxxooxoxxxxxxoooxxxxxxxxoxoooooooo","o",20)
"""

