print("\n[week13] Heap Sort\n")

print("<1> Heap - Each Data to be Entered")


class Heap:
    def __init__(self, array):  # heap initialization
        self.S = array          # array to save 'heap'
        self.heap_size = 0      # size of heap
        self.move_count = 0     # number of moves

    def siftUp(self, i):        # to maintain heap property
        while (i > 1) and (self.S[i // 2] < self.S[i]):
            # (not root) & (parent < child) -> exchange
            self.S[i // 2], self.S[i] = self.S[i], self.S[i // 2]
            i //= 2             # index update
            self.move_count += 1

    def siftDown(self, i):      # to maintain heap property
        siftkey = self.S[i]     # save current element
        parent = i
        right_spot = False      # check if proper place or not
        while (parent * 2 <= self.heap_size) and (not right_spot):
            if (parent * 2 < self.heap_size) and (self.S[2 * parent] < self.S[2 * parent + 1]):
                largerchild = 2 * parent + 1    # 'right' child
            else:
                largerchild = 2 * parent        # 'left' child
            if (siftkey < self.S[largerchild]):
                self.S[parent] = self.S[largerchild]
                parent = largerchild
                self.move_count += 1
            else:   # found right place
                right_spot = True
        self.S[parent] = siftkey

    def root(self):
        keyout = self.S[1]     # save root
        self.S[1] = self.S[self.heap_size]  # last element to root
        self.heap_size -= 1
        self.siftDown(1)    # maintain heap property
        return keyout       # return 'root'

    def addElt(self, elt):  # add new element to heap
        self.heap_size += 1
        if (self.heap_size < len(self.S)):  # size check
            self.S[self.heap_size] = elt    # add new element to 'heap'
        else:   # not enough
            self.S.append(elt)  # add new element to 'array'
        self.siftUp(self.heap_size) # maintain heap property

def makeHeap1(H):   # method 1
    H.heap_size = len(H.S) - 1  # first element 'dummy'
    for i in range(2, H.heap_size + 1): # second ~ last
        H.siftUp(i) # new element added -> siftUp

def makeHeap2(H):   # method 2
    H.heap_size = len(H.S) - 1  # first element 'dummy'
    for i in range(H.heap_size // 2, 0, -1):    # middle to root (inverse)
        H.siftDown(i)   # parent > child


def heapSort1(array):
    H = Heap(array)
    makeHeap1(H)
    sorted_array = []
    while (H.heap_size > 0):
        sorted_array.append(H.root())
    return sorted_array

# a = [0, 11, 14, 2, 7, 6, 3, 9, 5]
a = [0, 5, 9, 2, 17, 6, 13, 11, 7, 15]
print(f"a = {a}")

b = Heap(a)
makeHeap1(b)
print(f">>> number of moves: {b.move_count}")

result1 = heapSort1(a)
print(f">>> heap sort result: {result1}")

print()
print()

print("<2> Heap - All Data in Tree")

def heapSort2(H):
    makeHeap2(H)
    sorted_array = []
    for i in range(len(H.S) - 1, 0, -1):
        sorted_array.append(H.root())
    return sorted_array


# a = [0, 11, 14, 2, 7, 6, 3, 9, 5]
a = [0, 5, 9, 2, 17, 6, 13, 11, 7, 15]
print(f"a = {a}")

c = Heap(a)
makeHeap2(c)
print(f">>> number of moves: {c.move_count}")

result2 = heapSort2(c)
print(f">>> heap sort result: {result2}")

print()