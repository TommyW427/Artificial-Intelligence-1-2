# Name: Tommy Williams    Date: 10/14/2021
import random, time, math
from queue import PriorityQueue
import heapq;

class HeapPriorityQueue():
   def __init__(self):
      self.queue = ["dummy"]  # we do not use index 0 for easy index calulation
      self.current = 1        # to make this object iterable

   def next(self):           
      if self.current >= len(self.queue):
         self.current = 1     # to restart iteration later
         raise StopIteration
    
      out = self.queue[self.current]
      self.current += 1
   
      return out

   def __iter__(self):
      return self

   __next__ = next

   def isEmpty(self):
      return len(self.queue) == 1    # b/c index 0 is dummy

   def swap(self, a, b):
      self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

   def push(self, value):
      self.queue.append(value)
      self.heapUp(len(self.queue)-1)

   # helper method for push      
   def heapUp(self, k):
      while True:
         if k<=1:
             return
         pIndex = k//2
         parent = self.queue[pIndex]
         node = self.queue[k]
         if node<parent:
             self.swap(k,pIndex)
             k=pIndex
         else:
            return
               
        
   
   # remove the min value (root of the heap)
   # return the removed value            
   def pop(self):
      return self.remove(0)
      #self.remove(self.queue.index(min(self.queue[1:])))
      
   # remove a value at the given index (assume index 0 is the root)
   # return the removed value   
   def remove(self, index):
      index = index+1
      self.swap(index,len(self.queue)-1)
      t = self.queue.pop(len(self.queue)-1)
      k=index
      size = len(self.queue)-1
      while 2*k<=size:
         left,right = 2*k,2*k+1
         if max(left,right)>size: 
            if not left>size: right=left 
            else: return t
         lNode,rNode = self.queue[left],self.queue[right]
         node = self.queue[k]
         if min(lNode,rNode)==rNode and node>rNode:
            self.swap(k,right)
            k=right
         elif min(lNode,rNode)==lNode and node>rNode:
            self.swap(k,left)
            k=left
         else:
            return t
         

      return t
   
def isHeap(heap, k):
   left, right = 2*k, 2*k+1
   if left == len(heap): return True
   elif len(heap) == right and heap[k] > heap[left]: return False
   elif right < len(heap): 
      if (heap[k] > heap[left] or heap[k] > heap[right]): return False
      else: return isHeap(heap, left) and isHeap(heap, right)
   return True         

def inversion_count(new_state, width = 4, N = 4):
   ''' 
   Depends on the size(width, N) of the puzzle, 
   we can decide if the puzzle is solvable or not by counting inversions.
   If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
   If N is even, puzzle instance is solvable if
      the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is even.
      the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is odd.
   ''' 
   blankPos=new_state.index("_")
   blankRow=blankPos//N
   count=0
   new_state = new_state.replace("_","")
   for i in range(len(new_state)):
       for a in range(i+1,len(new_state)):
           if new_state[i]>new_state[a]:
              count+=1
   if N%2==1: return True if count%2==0 else False
   else: return True if (blankRow)%2==0 and count%2==0 or (blankRow)%2==1 and count%2==1 else False
 

def check_inversion():
   t1 = inversion_count("_42135678", 3, 3)  # N=3
   f1 = inversion_count("21345678_", 3, 3)
   t2 = inversion_count("4123C98BDA765_EF", 4) # N is default, N=4
   f2 = inversion_count("4123C98BDA765_FE", 4)
   return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
   sample_list = list(sample)
   random.shuffle(sample_list)
   new_state = ''.join(sample_list)
   while not inversion_count(new_state, size, size): 
      random.shuffle(sample_list)
      new_state = ''.join(sample_list)
   print(new_state)
   return new_state
   
def swap(n, i, j):
   l = list(n)
   l[i],l[j] = l[j],l[i]
   return "".join(l)
      
'''Generate a list which hold all children of the current state
   and return the list'''
def generate_children(state, size=4):
   children = ()
   #0 1 2 3
   #4 5 6 7
   #8 9 A B
   #C D E F

   #C 4 9 1
   #_ 3 5 B
   #A F E 2
   #8 6 7 D
   swapList = ((1,4),(0,2,5),(1,3,6),(2,7), \
               (0,8,5),(1,4,6,9),(2,5,10,7),(3,6,11), \
               (4,9,12),(5,8,10,13),(6,9,11,14),(7,10,15), \
               (8,13),(9,12,14),(10,13,15),(11,14))
   #strToNum = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,\
               #"8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
   a=state.index("_")
   b=swapList[a]
   for i in b:
      n = int(state[i],16)
      children+=((swap(state,a,i),abs(a//size-n//size)>abs(i//size-n//size) \
                      or abs(a%size-n%size)>abs(i%size-n%size)),)
   ##DISGUSTINGNESS##
   #return ((swap(state,a,i),abs(a//size-(n:=int(state[i],16))//size)>abs(i//size-n//size) \
                      #or abs(a%size-n%size)>abs(i%size-n%size)) for i in b)
   return children

def display_path(path_list, size):
   for n in range(size):
      for path in path_list:
         print (path[n*size:(n+1)*size], end = " "*size)
      print ()
   print ("\nThe shortest path length is :", len(path_list))
   return ""

   


''' You can make multiple heuristic functions '''
def dist_heuristic(state, goal = "_123456789ABCDEF", size=4):
   
   # manhattan distance#
   # _ 1 2 3#      # _ 4 8 C#
   # 4 5 6 7#      # 1 5 9 D#s
   # 8 9 A B#
   # C D E F#
   c = 0
   num = 0
   for i in range(size*size):
      if state[i] != "_":
         num = int(state[i], 16)
         c += abs(num % size - i % size) + abs(num // size - i // size)
   return c


#def man(i,size,num):
#   return abs(num % size - i % size) + abs(num // size - i // size)

def check_heuristic():
   a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
   b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
   return (a < b) 

def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size = 4):
   #if not inversion_count(start): return None
   #frontier = HeapPriorityQueue()
   frontier = PriorityQueue()
   if start == goal: return []
   state = start[:]
   h=dist_heuristic(state,size)
   #frontier.push((h,state,[state]))
   frontier.put((h,state,[state]))
   explored = set(state)
   while True:
      if frontier.empty(): return None
      ste = frontier.get()
      state = ste[1]
      path = ste[2]
      if state == goal: return path
      #print(path)
      for a in generate_children(state,size):
          if (not a in explored):# and heuristic(a)<=heuristic(state)+1:
             explored.add(a)
             frontier.put((heuristic(a,size)+len(path),a,path+[a]))
             
def solve(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size = 4):
   #frontier = PriorityQueue()
   frontier = []
   if start == goal: return []
   h=dist_heuristic(start,size)
   heapq.heappush(frontier,(h,start,(start,)))
   explored = set(start)
   while True:
      #if len(frontier) == 0: return None
      ch,state,path = heapq.heappop(frontier)
      if state in goal: return path
      for a,b in generate_children(state,size):
          if not (a in explored):
             explored.add(a)
             newCh = ch
             if b: newCh+=2
             #if newCh!=heuristic(a):
                #print(heuristic(a),newCh)
                #print(state[0:4] + " " + a[0:4])
                #print(state[4:8] + " " + a[4:8])
                #print(state[8:12] + " " + a[8:12])
                #print(state[12:16] + " " + a[12:16])
             heapq.heappush(frontier,(newCh,a,path+(a,)))
             #frontier.put((heuristic(a,size)+len(path),a,path+[a],heuristic(a)))
   return None

def main():
    # A star
   print ("Inversion works?:", check_inversion())
   print ("Heuristic works?:", check_heuristic())
   initial_state = input("Type initial state: ")
   
   if inversion_count(initial_state,4,4):
      cur_time = time.time()
      path = (solve(initial_state))
      if path != None:
         display_path(path, 4)
      else: print ("No Path Found.")
      print ("Duration: ", (time.time() - cur_time))
   else: print ("{} did not pass inversion test.".format(initial_state))
   
if __name__ == '__main__':
   main()

