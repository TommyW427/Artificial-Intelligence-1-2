# Name:  Tommy Williams        Date: 10/5/21
import time
import string
from queue import PriorityQueue


class HeapPriorityQueue():
    def __init__(self):
        self.queue = ["dummy"]  # we do not use index 0 for easy index calulation
        self.current = 1  # to make this object iterable

    def next(self):  # define what __next__ does
        if self.current >= len(self.queue):
            self.current = 1  # to restart iteration later
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 1  # b/c index 0 is dummy

    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

    # Add a value to the heap_pq
    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)

    # helper method for push
    def heapUp(self, k):
        if k <= 1:
            return
        pIndex = k // 2
        parent = self.queue[pIndex]
        node = self.queue[k]
        if node < parent:
            self.swap(k, pIndex)
            self.heapUp(pIndex)
        return

    # helper method for reheap and pop
    def heapDown(self, k, size):
        left, right = 2 * k, 2 * k + 1
        if max(left, right) > size:
            if not left > size:
                right = left
            else:
                return
        lNode, rNode = self.queue[left], self.queue[right]
        node = self.queue[k]
        if min(lNode, rNode) == rNode and node > rNode:
            self.swap(k, right)
        elif min(lNode, rNode) == lNode and node > rNode:
            self.swap(k, left)

    # make the queue as a min-heap
    def reheap(self):
        # heapDown(1,len(self.queeu)-1)
        for i in range(1, (len(self.queue) + 1) // 2 + 1):
            self.heapDown(i, len(self.queue) - 1)

    # remove the min value (root of the heap)
    # return the removed value
    def pop(self):
        return self.remove(self.queue[1:].index(min(self.queue[1:])))

    # remove a value at the given index (assume index 0 is the root)
    # return the removed value
    def remove(self, index):
        index = index + 1
        self.swap(index, len(self.queue) - 1)
        t = self.queue.pop(len(self.queue) - 1)
        self.reheap()

        return t


def generate_adjacents(current, words_set):
    ''' words_set is a set which has all words.
    By comparing current and words in the words_set,
    generate adjacents set of current and return it'''
    adj_list = set()
    for a in range(len(current)):
        for b in string.ascii_lowercase:
            if b != current[a]:
                testWord = current[:a] + b + current[a + 1:]
                if testWord in words_set:
                    adj_list.add(testWord)
    return adj_list


def check_adj(words_set):
    # This check method is written for words_6_longer.txt
    adj = generate_adjacents('listen', words_set)
    target = {'listee', 'listel', 'litten', 'lister', 'listed'}
    return (adj == target)


def display_path(n,gExplored,sExplored):  # key: current, value: parent
    l = []
    h = n
    k=h
    while gExplored[n][0] != "g":  # "s" is initial's parent
        l.append(n)
        n = gExplored[n][0]
    l.append(n)
    j = []
    while sExplored[h][0] != "s":
        j.append(h);
        h = sExplored[h][0];
    j = j[::-1]
    return [k] + j+l[1:]

def h(state,goal):
    count = 0
    for i in range(len(state)):
        if not (state[i]==goal[i]): count+=1
    return count

def a_star(start, goal, word_set):
   frontier = PriorityQueue()
   explored = set(start)
   if start == goal: return []
   state = start[:]
   aitch=h(state,goal)
   frontier.put((aitch,state,[state]))
   while True:
      if frontier.empty(): return []
      ste = frontier.get()
      state = ste[1]
      path = ste[2]
      if state == goal: return path
      for a in generate_adjacents(state,word_set):
          if not (a in explored):
             explored.add(a)
             frontier.put((h(a,goal)+len(path),a,path+[a]))

def main():
    filename = input("Type the word file: ")
    words_set = set()
    file = open(filename, "r")
    for word in file.readlines():
        words_set.add(word.rstrip('\n'))
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    print(check_adj(words_set))
    cur_time = time.time()
    path = (a_star(initial, goal, words_set))
    if path != None:
        print(path)
        print("The number of steps: ", len(path))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()
