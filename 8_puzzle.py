import time
from datetime import datetime

now = datetime.now()
print '%s/%s/%s %s:%s:%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

#declare goal as a global variable
goal = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
#declaring range as three
n=3

#function to define Manhattan Distance Heuristic
def man_dist(puzzle):
    mand = 0
    for i in range(n):
        for j in range(n):
            count = puzzle.retrive(i, j) - 1
            if (count == 0):
                continue
            x = abs((count-1)/n)
            y = (count - 1) % n
            mand = mand + abs(x - i) + abs(y - j)
            #print "The Manhattan Distance is" + str(mand)
    return mand

#function to define Misplaced Tile Heuristic
def misplaced_tile(puzzle):
    mispl = 0
    for i in range(n):
        for j in range(n):
            if (puzzle.retrive(i, j)-1)!= (goal[i][j]):
                mispl += 1
                #print "The Misplaced Tiles are" + str(mispl)
    return mispl

#function to define Uniform cost search where heuristic is equal to zero
def ucst(puzzle):
    puzzle=puzzle
    return 0






#define a class which describes different features of the Node
class Node:

    def __init__(self,h_score=0, depth=0, parent= None):
        self.h_score = h_score
        self.depth = depth
        self.parent = parent
        self.state = []
        for i in range(n):
            self.state.append(goal[i][:])

    def astar(self, heuristic):

        def solvable(puzzle):
            if puzzle.state == goal:
                return 1

        openlist = [self]
        closedlist = []
        move_count = 0
        while len(openlist):
            x = openlist.pop(0)
            move_count += 1
            if (solvable(x)):
                if len(closedlist):
                    return x.goal_path([]), move_count
                else:
                    return [x]

            successor = x.moves()
            for move in successor:
                neighbour = index(move, openlist)
                visited = index(move, closedlist)
                hval = heuristic(move)
                fval = hval + move.depth
                if visited == -1 and neighbour == -1:
                    move.h_score = hval
                    openlist.append(move)
                elif neighbour > -1:
                    copy = openlist[neighbour]
                    if fval < copy.h_score + copy.depth:
                        copy.h_score = hval
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif visited > -1:
                    copy = closedlist[visited]
                    if fval < copy.h_score + copy.depth:
                        move.h_score = hval
                        closedlist.remove(copy)
                        openlist.append(move)

            closedlist.append(x)
            openlist = sorted(openlist, key=lambda p: p.h_score + p.depth)

        return [], 0


    def __eq__(self, diff):
        if self.__class__ != diff.__class__:
            return 0
        else:
            return self.state == diff.state

    def __str__(self):
        res = ''
        for row in range(n):
            res += ' '.join(map(str, self.state[row]))
            res += '\r\n'
        return res

    def clone(self):
        p = Node()
        for i in range(n):
            p.state[i] = self.state[i][:]
        return p

    #this function identifies the indices where the zero can move and appends it to free
    def blank_moves(self):
        row, col = self.find(0)
        free = []
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

        # find the index of zero which is present in the given array
    def find(self, value):
        for row in range(n):
           for col in range(n):
              if self.state[row][col] == value:
                 return row, col

    def moves(self):
        free = self.blank_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self.clone()
            p.swap(a, b)
            p.depth = self.depth + 1
            #print("depth of Algorithm is" + str(p.depth))
            p.parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)


    #returns the index of rows and column
    def retrive(self, row, col):
        return self.state[row][col]

    #assign values to the row and column indices
    def assign(self, row, col, value):
        self.state[row][col] = value

    # swap the position of the zero and the position where the zero can move
    def swap(self, pos_a, pos_b):
        temp = self.retrive(*pos_a)
        self.assign(pos_a[0], pos_a[1], self.retrive(*pos_b))
        self.assign(pos_b[0], pos_b[1], temp)

    def goal_path(self, path):
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.goal_path(path)

def index(item, seq):
    if item in seq:
        return seq.index(item)
    else:
        return -1


#Defining the MAIN function
def main():

    p = Node()

    trivial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    very_easy = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    easy = [1, 2, 3, 4, 8, 0, 7, 6, 5]
    doable = [0, 1, 2, 4, 5, 3, 7, 8, 6]
    oh_boy = [8, 7, 1, 6, 0, 2, 5, 4, 3]
    impossible = [1, 2, 3, 4, 5, 6, 8, 7, 0]

    print "Welcome to 8-Puzzle"
    print "Please enter your choice of puzzle \n1. Trivial \n2. Very_Easy \n3. Easy \n4. Doable \n5. Oh_boy\n6. Impossible\n7. any type of combination you want to add"
    x = input("Enter your Choice -> ")
    print x

    if(x == 1):
        inputVaribale = trivial
        print "The input entered is already solved"
        exit()
    elif (x == 2):
        inputVaribale = very_easy
    elif (x == 3):
        inputVaribale = easy
    elif (x == 4):
        inputVaribale = doable
    elif (x == 5):
        inputVaribale = oh_boy
    elif (x == 6):
        inputVaribale = impossible
        print "This state cannot be solved"
        exit()
    else:
        #add the elements in an array to design your own puzzle
        array= list()
        print ('Enter the type of a random puzzle to be solved')
        for i in range(9):
            n= input("number:")
            array.append(int(n))
        print 'Array:'+ str(array)
        inputVaribale= array


    #take in the indices of the rows and column of the matrix
    locations1 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    locations2 = [0, 1, 2, 0, 1, 2, 0, 1, 2]

    #assign the values taken from the input array to the indices of the array
    for i in range(9):
        p.assign(locations1[i], locations2[i], inputVaribale[i])
    print p


    print "Three types of algorithm are:\n 1. Uniform Cost Search \n 2. Misplaced Tile Heuristic\n 3. Manhattan Distance"
    a = input('Enter the type of algorithm to perform')
    # start the timer
    start = time.time()

    if (a==1):
        path, numbers = p.astar(ucst)
        path.reverse()
        for i in path:
            print i
        print "Uniform Cost Search takes " + str(numbers)+ " states"

    if (a== 2):
       path,numbers = p.astar(misplaced_tile)
       path.reverse()
       for i in path:
          print i
       print "A Star with Mispalced Tile Heuristic " + str(numbers) +" states"

    if (a ==3):
        path, numbers = p.astar(man_dist)
        path.reverse()
        for i in path:
            print i
        print "A Star with Manhattan distance Heuristic " + str(numbers)+ " states"

    # end the timer
    end = time.time()
    # calculate the time elapsed and print it
    elapsed = end - start
    print "\n time elapsed " + str(elapsed) + " seconds"

if __name__ == "__main__":
    main()