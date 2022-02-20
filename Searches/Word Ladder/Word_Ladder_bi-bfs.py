# Name:  Tommy Williams        Date: 10/5/21
import time
import string

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


def display_path(n, sExplored,gExplored):  # key: current, value: parent
    l = []
    h = n
    while gExplored[n] != "g":  # "s" is initial's parent
        l.append(n)
        n = gExplored[n]
    l.append(n)

    j = []
    while sExplored[h] != "s":
        j.append(h)
        h = sExplored[h]
    j.append(h)
    j=j[::-1]
    l = j+l[1:]


    # for i in l:
    #   print (i)
    return l


def bi_bfs(start, goal, words_set):
    '''The idea of bi-directional search is to run two simultaneous searches--
    one forward from the initial state and the other backward from the goal--
    hoping that the two searches meet in the middle.
    '''
    if start == goal: return []
    sQ = [start]
    gQ = [goal]
    gExplored = {goal:"g"}
    sExplored = {}
    sExplored[start] = "s"
    while True:
        if len(sQ) == 0 or len(gQ)==0:
            return "No solution", "NA"
        state = sQ.pop(0)
        gState = gQ.pop(0)

        if gState in sExplored:
            return display_path(gState,sExplored,gExplored)
        elif state in gExplored:
            return display_path(state,sExplored,gExplored)

        for a in generate_adjacents(state, words_set):
            if not (a in sExplored):
                sQ.append(a)
                sExplored[a] = state
        for b in generate_adjacents(gState, words_set):
            if not (b in gExplored):
                gQ.append(b)
                gExplored[b] = gState

    return None


def main():
    filename = input("Type the word file: ")
    words_set = set()
    file = open(filename, "r")
    for word in file.readlines():
        words_set.add(word.rstrip('\n'))
    # print ("Check generate_adjacents():", check_adj(words_set))
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path = (bi_bfs(initial, goal, words_set))
    if path != None:
        print(path)
        print("The number of steps: ", len(path))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()
