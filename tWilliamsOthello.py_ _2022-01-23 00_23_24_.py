# Name: Tommy Williams 
# Date: 1/18/2022

import copy
import random

class RandomBot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      print(self.stones_left)
      moves = self.find_moves(board,color)
      print(moves.keys())
      best_move = random.choice(list(moves.keys()))
      
      print(moves[best_move])
      self.flipPieces(board,moves[best_move],color)
      print(best_move)
      return best_move, 0 if color=="@" else 1

   def stones_left(self, board):
      count = 0
      for col in board:
         for pos in col:
            if pos=='.':
               count+=1
      return count

   def flipPieces(self,board,pieces,color):
      for p in pieces:
         board[p[0]][p[1]]=color
      return

   def getAdjacents(self, x, y):
      moves = ()
      for d in self.directions:
         dx = x+d[0]
         dy = y+d[1]
         if dy<self.y_max and dy>=0 and dx<self.x_max and dx>=0:
            moves += ((dx, dy, d),)
      return moves

   def find_moves(self, board, color):
      moves = {}
      for x in range(len(board)):
         for y in range(len(board[x])):
            if board[x][y]=='.':
               for dx,dy,d in self.getAdjacents(x,y):
                  if board[dx][dy] == self.opposite_color[color]:
                     print(x,y,d)
                     returner = self.find_flipped(board,x,y,color)
                     print(returner)
                     if len(returner)>0:
                        moves[returner[-1]] = returner[:-1]                 
      return moves

   def recursiveSquabbleDobble(self,board,x,y,dx,dy,color,d):
      flipped = []
      if dx<self.x_max and dx>=0 and dy<self.y_max and dy>=0:
         if board[dx][dy] == self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,dx,dy,dx+d[0],dy+d[1],color,d)
            if returner==False: return False
            else:
               returner.append((x,y))
               return returner

         elif board[dx][dy] == color:
            return [(x,y)]
      return False
      
   def find_flipped(self, board, x, y, color):
      flipped = []
      for dx,dy,d in self.getAdjacents(x,y):
         if board[dx][dy]==self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,x,y,dx,dy,color,d)
            if returner != False: flipped = flipped + returner
      return flipped

class Minimax_AI_bot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.weightedBoard = [[10,-3,2,2,2,2,-3,10],[-3,-4,-1,-1,-1,-1,-4,-3],[2,-1,1,0,0,1,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,1,0,0,1,-1,2],[-3,-4,-1,-1,-1,-1,-4,-3],[10,-3,2,2,2,2,-3,10]]

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      #print(self.stones_left(board))
      moves = self.find_moves(board,color)
      #print(moves.values())
      #print(moves.keys())
      best_move = self.minimax(board,color,[],3)
      #print(best_move)
      return best_move[1], 0 if color=="@" else 1

   def minimax(self, board, color, prevMove, search_depth):
      moves = self.find_moves(board,color)
      #print("\n" + str(search_depth))
      #print(moves)
      if search_depth == 0 or len(moves.keys())==0:
         return self.evaluate(board,color,[]),[]  #add in find_moves later
      v = -999
      for s in moves.keys():
         tempState = self.fake_move(board,color,s,moves[s])
         w,tr = self.minimax(tempState,self.opposite_color[color],s,search_depth-1)
         w = -1*w
         if w>v:
            best_move = s
            v = w
      return v, best_move

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      pass

   def make_key(self, board, color):
    # hashes the board
      return 1

   def stones_left(self, board):
      count = 0
      for col in board:
         for pos in col:
            if pos=='.':
               count+=1
      return count

   def fake_move(self, board, color, move, flipped):
      fakeBoard = copy.deepcopy(board)
      for p in flipped:
         fakeBoard[p[0]][p[1]] = color
      fakeBoard[move[0]][move[1]] = color
      return fakeBoard

   def make_move(self, board, color, move, flipped):
      for p in flipped:
         board[p[0]][p[1]] = color
      board[move[0]][move[1]] = color
      return 1

   def placementValue(self,board,color):
      evalY, evalN, totalY, totalN = 0, 0, 0, 0
      for x in range(len(board)):
         for y in range(len(board[x])):
            if board[x][y] == color:
               evalY += self.weightedBoard[x][y]
               totalY += 1
            elif board[x][y] == self.opposite_color[color]:
               evalN += self.weightedBoard[x][y]
               totalN += 1
      return evalY-evalN

   def manuevarability(self,board,color,possible_moves):
      #return possible_moves-find_moves()
      return 1

   def stability(self,board,color):
      return 1

   def evaluate(self, board, color, possible_moves):
      return self.placementValue(board,color)

   def score(self, board, color):
    # returns the score of the board 
      return 1

   def stones_left(self, board):
      count = 0
      for col in board:
         for pos in col:
            if pos=='.':
               count+=1
      return count

   def flipPieces(self,board,pieces,color):
      for p in pieces:
         board[p[0]][p[1]]=color
      return

   def getAdjacents(self, x, y):
      moves = ()
      for d in self.directions:
         dx = x+d[0]
         dy = y+d[1]
         if dy<self.y_max and dy>=0 and dx<self.x_max and dx>=0:
            moves += ((dx, dy, d),)
      return moves

   def find_moves(self, board, color):
      moves = {}
      for x in range(len(board)):
         for y in range(len(board[x])):
            if board[x][y]=='.':
               for dx,dy,d in self.getAdjacents(x,y):
                  if board[dx][dy] == self.opposite_color[color]:
                     returner = self.find_flipped(board,x,y,color)
                     if len(returner)>0:
                        moves[returner[-1]] = returner[:-1]                 
      return moves

   def recursiveSquabbleDobble(self,board,x,y,dx,dy,color,d):
      flipped = []
      if dx<self.x_max and dx>=0 and dy<self.y_max and dy>=0:
         if board[dx][dy] == self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,dx,dy,dx+d[0],dy+d[1],color,d)
            if returner==False: return False
            else:
               returner.append((x,y))
               return returner

         elif board[dx][dy] == color:
            return [(x,y)]
      return False
      
   def find_flipped(self, board, x, y, color):
      flipped = []
      for dx,dy,d in self.getAdjacents(x,y):
         if board[dx][dy]==self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,x,y,dx,dy,color,d)
            if returner != False: flipped = flipped + returner
      return flipped

class Best_AI_bot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.weightedBoard = [[10,-3,3,3,3,3,-3,10],[-3,-6,-1,-1,-1,-1,-6,-3],[3,-1,1,0,0,1,-1,3],[3,-1,0,1,1,0,-1,3],[3,-1,0,1,1,0,-1,3],[3,-1,1,0,0,1,-1,3],[-3,-6,-1,-1,-1,-1,-6,-3],[10,-3,3,3,3,3,-3,10]]

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      newBoard = ""
      for y in range(len(board)):
         for x in range(len(board)):
            newBoard+=board[x][y]
      board = list(newBoard)
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      #print(self.stones_left(board))
      moves = self.find_moves(board,color)
      #print(moves.keys())
      best_move = self.minimax(board,color,[],3)
      print(best_move[0])
      #print(best_move)
      return best_move[1], 0 if color=="@" else 1

   def minimax(self, board, color, prevMove, search_depth):
      moves = self.find_moves(board,color)
      #print("\n" + str(search_depth))
      #print(moves)
      if search_depth == 0 or len(moves.keys())==0:
         return self.evaluate(board,color,moves),[]  #add in find_moves later
      v = -999
      for s in moves.keys():
         tempState = self.fake_move(board,color,s,moves[s])
         w,tr = self.minimax(tempState,self.opposite_color[color],s,search_depth-1)
         w = -1*w
         if w>v:
            best_move = s
            v = w
      return v, best_move

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      pass

   def make_key(self, board, color):
    # hashes the board
      return 1

   def fake_move(self, board, color, move, flipped):
      fakeBoard = copy.deepcopy(board)
      for p in flipped:
         fakeBoard[p[0]+p[1]*8] = color
      fakeBoard[move[0]+move[1]*8] = color
      return fakeBoard

   def make_move(self, board, color, move, flipped):
      for p in flipped:
         board[p[0]+p[1]*8] = color
      board[move[0]+move[1]*8] = color
      return 1

   def placementValue(self,board,color):
      evalY, evalN, totalY, totalN = 0, 0, 0, 0
      for z in range(len(board)):
         y,x = z//8,z%8
         if board[x+y*8] == color:
            evalY += self.weightedBoard[x][y]
            totalY += 1
         elif board[x+y*8] == self.opposite_color[color]:
            evalN += self.weightedBoard[x][y]
            totalN += 1
      return evalY-evalN

   def manuevarability(self,board,color,possible_moves):
      return len(possible_moves)-len(self.find_moves(board,self.opposite_color[color]))

   def stableCheck(self,board,x,y,color,direction,stables):
      #use self.directions
      stability = {}
      for d in self.directions:
         stability[d] = 1
      stability[direction] = 2
      stability[(-1*i for i in direction)] = 2
      for dx,dy,d in self.getAdjacents(x,y):
         while stability[d]==1: 
            if board[dx+dy*8]==color:
               if dx+dy*8 in stables or (dx+d[0]>=self.x_max or dx+d[0]<0 or dy+d[1]>=self.y_max or dy+d[1]<0):
                  stability[d] = 2
                  stability[(i*-1 for i in d)] = 2
                  break
            elif board[dx+dy*8]=='.':
               stability[d] = 1
               break
            else:
               stability[d] = 0
               break
            dx += d[0]
            dy += d[1]
      return 0 if 0 in stability.values() else 1 if 1 in stability.values() else 2

   """def iterativeComprehensiveStability(self,board,color):
      stables = set()
      semistables = set()
      for z in (0,7,56,63):
         if board[z] == color:
            stables.add(z)
      for z in range(len(board)):
         x,y = z%8,z//8"""     

   def recursiveStability(self,board,x,y,color,dir,stables):
      stableCount=0
      r = self.stableCheck(board,x,y,color,dir,stables)
      if (x+y*8) in stables or r==2:
         stables.add(x+8*y)
         stableCount+=2
         for dx,dy,d in self.getAdjacents(x,y):
            if board[dx+dy*8]==color and not (dx+dy*8) in stables:
               return self.recursiveStability(board,dx,dy,color,d,stables)
      elif r==2:
         stableCount+=1
      return stables

   def stability(self,board,color):
      cornerStables = set()

      for z in (0,7,56,63):
         if board[z] == color:
            cornerStables.add(z)
      stables = copy.deepcopy(cornerStables)
      
      for z in cornerStables:
         x,y = z%8,z//8
         stables = self.recursiveStability(board,x,y,color,(0,0),stables)
      return len(stables)*2

   def evaluate(self, board, color, possible_moves):
      opp_moves = self.find_moves(board,self.opposite_color[color]).keys()
      p = self.placementValue(board,color)
      m = self.manuevarability(board,color,possible_moves)
      s = self.stability(board,color)-self.stability(board,self.opposite_color[color])
      d = self.capturability(board,color)-self.capturability(board,self.opposite_color[color])
      c = 0
      for corner in ((0,0),(0,7),(7,0),(7,7)):
         if corner in possible_moves: c+=10
         elif corner in opp_moves: c-=10
      return p+m+d+c

   def score(self, board, color):
    # returns the score of the board 
      return 1

   def capturability(self,board,color):
      nonCapturable = 0
      rSetFlipped = set()
      revFlipped = self.find_moves(board,self.opposite_color[color]).values()
      for z in revFlipped:
         #print(z)
         #print(set(z))
         rSetFlipped = rSetFlipped.union(set(z))
      #print(rSetFlipped)
      for z in range(len(board)): 
         if board[z] == color:
            x,y = z%8,z//8
            if not (x,y) in rSetFlipped:
               nonCapturable+=1
      return nonCapturable

   def stones_left(self, board):
      count = 0
      for pos in board:
            if pos=='.':
               count+=1
      return count

   def flipPieces(self,board,pieces,color):
      for p in pieces:
         board[p[0]+p[1]*8]=color
      return

   def getAdjacents(self, x, y):
      moves = ()
      for d in self.directions:
         dx = x+d[0]
         dy = y+d[1]
         if dy<self.y_max and dy>=0 and dx<self.x_max and dx>=0:
            moves += ((dx, dy, d),)
      return moves

   def find_moves(self, board, color):
      moves = {}
      for z in range(len(board)):
         y,x = z//8,z%8
         if board[z]=='.':
            for dx,dy,d in self.getAdjacents(x,y):
               if board[dx+dy*8] == self.opposite_color[color]:
                  returner = self.find_flipped(board,x,y,color)
                  if len(returner)>0:
                     moves[returner[-1]] = returner[:-1]                 
      return moves

   def recursiveSquabbleDobble(self,board,x,y,dx,dy,color,d):
      flipped = []
      if dx<self.x_max and dx>=0 and dy<self.y_max and dy>=0:
         if board[dx+dy*8] == self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,dx,dy,dx+d[0],dy+d[1],color,d)
            if returner==False: return False
            else:
               returner.append((x,y))
               return returner

         elif board[dx+dy*8] == color:
            return [(x,y)]
      return False
      
   def find_flipped(self, board, x, y, color):
      flipped = []
      for dx,dy,d in self.getAdjacents(x,y):
         if board[dx+dy*8]==self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,x,y,dx,dy,color,d)
            if returner != False: flipped = flipped + returner
      return flipped

class Strategy:

   def __init__(self):
      self.white = "o"
      self.black = "x"
      self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 8
      self.y_max = 8
      self.logging = True
      self.weightedBoard = [[10,-3,2,2,2,2,-3,10],[-3,-6,-1,-1,-1,-1,-6,-3],[2,-1,1,0,0,1,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,1,0,0,1,-1,2],[-3,-6,-1,-1,-1,-1,-6,-3],[10,-3,2,2,2,2,-3,10]]

   def best_strategy(self, board, color,best_move,still_running,time_limit):
      #print("time", time_limit)
      # returns best move
      board = list(board)
      if color == "#000000" or color == "x":
         color = "x"
      else:
         color = "o"
      
      depth=1
      while best_move.value!=None or still_running:
         b = self.minimax(board,color,[],depth)[1]
         best_move.value = b[1]*8+b[0]
         depth+=1
      return best_move.value

   def minimax(self, board, color, prevMove, search_depth):
      moves = self.find_moves(board,color)
      #print("\n" + str(search_depth))
      #print(moves)
      if search_depth == 0 or len(moves.keys())==0:
         return self.evaluate(board,color,moves),[]  #add in find_moves later
      v = -999
      for s in moves.keys():
         tempState = self.fake_move(board,color,s,moves[s])
         w,tr = self.minimax(tempState,self.opposite_color[color],s,search_depth-1)
         w = -1*w
         if w>v:
            best_move = s
            v = w
      return v, best_move

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      pass

   def make_key(self, board, color):
    # hashes the board
      return 1

   def fake_move(self, board, color, move, flipped):
      fakeBoard = copy.deepcopy(board)
      for p in flipped:
         fakeBoard[p[0]+p[1]*8] = color
      fakeBoard[move[0]+move[1]*8] = color
      return fakeBoard

   def make_move(self, board, color, move, flipped):
      for p in flipped:
         board[p[0]+p[1]*8] = color
      board[move[0]+move[1]*8] = color
      return 1

   def placementValue(self,board,color):
      evalY, evalN, totalY, totalN = 0, 0, 0, 0
      for z in range(len(board)):
         y,x = z//8,z%8
         if board[x+y*8] == color:
            evalY += self.weightedBoard[x][y]
            totalY += 1
         elif board[x+y*8] == self.opposite_color[color]:
            evalN += self.weightedBoard[x][y]
            totalN += 1
      return evalY-evalN

   def manuevarability(self,board,color,possible_moves):
      return len(possible_moves)-len(self.find_moves(board,self.opposite_color[color]))

   def stableCheck(self,board,x,y,color,direction,stables):
      #use self.directions
      stability = {}
      for d in self.directions:
         stability[d] = False
      stability[direction] = True
      stability[(-1*i for i in direction)] = True
      for dx,dy,d in self.getAdjacents(x,y):
         while stability[d]==False: 
            if board[dx+dy*8]==color:
               if dx+dy*8 in stables or (dx+d[0]>=self.x_max or dx+d[0]<0 or dy+d[1]>=self.y_max or dy+d[1]<0):
                  stability[d] = True
                  stability[(i*-1 for i in d)] = True
                  break
            elif board[dx+dy*8]=='.':
               stability[d] = False
               break
            else:
               stability[d] = False
               break
            dx += d[0]
            dy += d[1]
      return not False in stability.values()

   def recursiveStability(self,board,x,y,color,dir,stables):
      if (x+y*8) in stables or self.stableCheck(board,x,y,color,dir,stables):
         stables.add(x+8*y)
         for dx,dy,d in self.getAdjacents(x,y):
            if board[dx+dy*8]==color and not (dx+dy*8) in stables:
               return self.recursiveStability(board,dx,dy,color,d,stables)
      return stables

   def stability(self,board,color):
      stableCount = 0
      stables = set()
      for z in (0,7,56,63):
         if board[z] == color:
            stables.add(z)
      for z in stables:
         x,y = z%8,z//8
         stables = self.recursiveStability(board,x,y,color,0,stables)
      return len(stables)*2

   def capturability(self,board,color):
      nonCapturable = 0
      rSetFlipped = set()
      revFlipped = self.find_moves(board,self.opposite_color[color]).values()
      for z in revFlipped:
         rSetFlipped = rSetFlipped.union(set(z))
      for z in range(len(board)): 
         if board[z] == color:
            x,y = z%8,z//8
            if not (x,y) in rSetFlipped:
               nonCapturable+=1
            else:
               nonCapturable-=1
      return nonCapturable

   def evaluate(self, board, color, possible_moves):
      opp_moves = self.find_moves(board,self.opposite_color[color]).keys()
      p = self.placementValue(board,color)
      m = self.manuevarability(board,color,possible_moves)
      s = self.stability(board,color)-self.stability(board,self.opposite_color[color])
      d = self.capturability(board,color)-self.capturability(board,self.opposite_color[color])
      c = 0
      for corner in ((0,0),(0,7),(7,0),(7,7)):
         if corner in possible_moves: c+=10
         elif corner in opp_moves: c-=10
      return p+m+d

   def score(self, board, color):
    # returns the score of the board 
      return 1

   def stones_left(self, board):
      count = 0
      for pos in board:
            if pos=='.':
               count+=1
      return count

   def flipPieces(self,board,pieces,color):
      for p in pieces:
         board[p[0]+p[1]*8]=color
      return

   def getAdjacents(self, x, y):
      moves = ()
      for d in self.directions:
         dx = x+d[0]
         dy = y+d[1]
         if dy<self.y_max and dy>=0 and dx<self.x_max and dx>=0:
            moves += ((dx, dy, d),)
      return moves

   def find_moves(self, board, color):
      moves = {}
      for z in range(len(board)):
         y,x = z//8,z%8
         if board[z]=='.':
            for dx,dy,d in self.getAdjacents(x,y):
               if board[dx+dy*8] == self.opposite_color[color]:
                  returner = self.find_flipped(board,x,y,color)
                  if len(returner)>0:
                     moves[returner[-1]] = returner[:-1]                 
      return moves

   def recursiveSquabbleDobble(self,board,x,y,dx,dy,color,d):
      flipped = []
      if dx<self.x_max and dx>=0 and dy<self.y_max and dy>=0:
         if board[dx+dy*8] == self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,dx,dy,dx+d[0],dy+d[1],color,d)
            if returner==False: return False
            else:
               returner.append((x,y))
               return returner

         elif board[dx+dy*8] == color:
            return [(x,y)]
      return False
      
   def find_flipped(self, board, x, y, color):
      flipped = []
      for dx,dy,d in self.getAdjacents(x,y):
         if board[dx+dy*8]==self.opposite_color[color]:
            returner = self.recursiveSquabbleDobble(board,x,y,dx,dy,color,d)
            if returner != False: flipped = flipped + returner
      return flipped
