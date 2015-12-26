#!/usr/bin/env python
from sys import *
import bit_io
import time

t0 = time.clock()

class Node:
    """Class for holding all node objects: branches and leaves.  For leaves,
       the left and right attributes are set to the value None while the
       char and weight attributes are set accordingly.  Branches are given
       a left and right attribute, which contain another node object
       recursively until a leaf is reached.  Branches' char and weight
       attributes are set to None, as our prefix coding system requires
       that all our values be at the leaf (end) nodes."""
    def __init__(self,char=None,weight=0,left=None,right=None):
        """Method to initialize a new node.  char, weight, left, and right
           are all set to None or 0 so that no leaf will have a branch
           protruding from it and so that no intermediate node is representing
           a character."""
        self.char = char # holds byte value
        self.weight = weight # holds a character's counts
        self.left = left # holds a node to which the current node points
        self.right = right # holds a node to which the current node points


def search_tree(tree,char,path=[]):
    if tree.char == char:
        result = tree.char
        return path
    if tree.left:
        result = search_tree(tree.left,char,path)
        path.append(0)
        if result != False:
            return result
        path.pop()
    if tree.right:
        result = search_tree(tree.right,char,path)
        path.append(1)
        if result != False:
            return result
        path.pop()

    return False
        

# make sure we're given the correct arguments
if len(argv) != 3:
    stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
    exit(2)

with open(argv[1], 'r') as input, bit_io.BitWriter(argv[2]) as output:
    # stores counts for each letter at the index corresponding to the letter's
    # ASCII byte value
    lines = input.readlines()
    alphabet = "".join(chr(x) for x in xrange(256)) # all 256 ASCII characters

    # number of times each character appears per line
    letter_counts = [[j.count(x) for j in lines] for x in alphabet]

    # total counts per ASCII character in entire file
    letter_counts = [sum(i) for i in letter_counts]
    print("sum(letter_counts): ", sum(letter_counts))

    # makes list of (char, count) tuples
    tuples = [(chr(i),letter_counts[i]) for i in xrange(len(letter_counts))]
#   tuples = sorted(tuples,key=lambda x: x[1]) # sorts, biggest last
    #print(tuples)

    # filters out elements that don't appear in file
    tuples = [i for i in tuples if i[1] != 0]

### Start working with forest below this line ###
    
    # makes list containing one node object for each character that appears
    # in the input file.  Node's args, i[0] and i[1], refer to the character
    # and the number of times it appears in the input file, respectively
    ascii_forest = [Node(i[0],i[1]) for i in tuples]

    # this section does all the merging into a single tree
    while len(ascii_forest) > 1:
        
        # these keep track of the smallest weights
        min_1_weight = ascii_forest[0].weight
        min_2_weight = ascii_forest[1].weight

        # these keep track of the most infrequent characters corresponding
        # to the above weights
        min_1_node = ascii_forest[0]
        min_2_node = ascii_forest[1]
        for i in xrange(len(ascii_forest)):
            if ascii_forest[i].weight < min_1_weight:
                if ascii_forest[i].weight < min_2_weight:
                    min_2_weight = ascii_forest[i].weight
                    min_2_node = ascii_forest[i]
                else:
                    min_1_weight = ascii_forest[i].weight
                    min_1_node = ascii_forest[i]
        new_node = Node(None,(min_1_weight+min_2_weight),min_1_node,min_2_node)
        ascii_forest.append(new_node) # stick newly-merged node into forest

        # remove the two nodes that were joined together
        # filter returns all values of the forest that satisfy the condition
        # that they aren't one of the two nodes we just joined together
        ascii_forest = filter(lambda x:x!=min_1_node,ascii_forest)
        ascii_forest = filter(lambda x:x!=min_2_node,ascii_forest)


    tree = ascii_forest[0] # put only remaining tree into simpler-to-use var
    encoding = [] # will hold each byte characters'encoded values
    for i in alphabet: # get encoding for each character
        # gets encoding in increasing byte order
        encoding.append(search_tree(tree,i,[]))


    encoding = [i for i in encoding if i != False] # encoding holds all encodings
    for int_list in xrange(len(encoding)):
        temp_string = ''
        for i in encoding[int_list]:
            temp_string += str(i)
        encoding[int_list] = temp_string

    # reverses direction of strings to make valid prefix code
    encoding = [i[::-1] for i in encoding]

    # NOTE: this is a currently a prefix code when the string of bits is read
    # from left to right; right to left is not a valid prefix code

    bits_written = 0
    # now, we must write the encoded values to the file
    output.writebits(len(encoding),8) # how many char encodings are there
    bits_written += 8
    #print("num chars: ",len(encoding))
    all_chars = [i[0] for i in tuples] # all the chars that are being encoded

    #print("tuples: ",tuples)
   # print(all_chars)
    #print("encoding: ",[int(i,2) for i in encoding])
    #print("encoding: ",encoding)
    #print([len(i) for i in encoding])
    #print("sum(encoding lengths): ",sum([len(i) for i in encoding]))

    # correctly writes all chars' binary representations to output
    # NOTE: encoding list should have same char ordering as all_chars
    for i in xrange(len(encoding)):
        # need to convert the string to series of 0s and 1s
        output.writebits(ord(all_chars[i]),8) # writes chars that are encoded
        output.writebits(len(encoding[i]),7) # length of encoding
        bits_written += 15
    #print("all_chars: ",[ord(i) for i in all_chars])
    #print("encoding lengths: ",[len(i) for i in encoding])

    print("bits_written: ",bits_written)
    print(len(encoding))
    for i in xrange(len(encoding)):
        # write each char's encoding
        output.writebits(int(encoding[i],2),len(encoding[i])) 
        bits_written += len(encoding[i])
    print("bits_written: ",bits_written)

    # since max possible length of an encoding is 128 bits, we can use 7 bits
    # to represent the lengths of the encodings
#    code_lengths = [bin(len(i))[2:] for i in encoding]
    # should write lengths of the all of the chars we're encoding
#    for i in code_lengths:
#        output.writebits(int(i,2),7)
    
#    print(lines)
#   print(all_chars)
    num_bytes = 0
    num_bits = 0
    input.seek(0)
    lines = input.readlines()
    num_lines = len(lines)
    num_spaces = 0
    for line in lines:
        num_spaces -= 1
        for word in line.split():
            num_spaces += 1
            for letter in word:
    #           #output.writebits(encoding[encoding.index(j)],)
    #           #output.writebits(int(encoding[all_chars.index(j)]),len(encoding[all_chars.index(j)]))
    #           #print(letter)
    #           print(encoding[all_chars.index(letter)])
                num_bytes += 1
                for bit in encoding[all_chars.index(letter)]:
    #               print(bit)
    #               output.writebit(bit)
                    num_bits += 1
    num_bytes += num_lines + num_spaces

    num_bits = 0
    i = 0
    while 1:
        for line in lines:
            for word in line:
                    buttz = ''
                    for bit in encoding[all_chars.index(word)]:
                        buttz += str(bit)
                    i+=len(buttz)
        num_bits = i
        print("num_bits (i version): ",i)
        break
    output.writebits(num_bits,64)
    output.writebits(num_bytes,64)
    print("num_bits: ",num_bits)
    print("num_bytes: ",num_bytes)
    
    input.seek(0)
    lines = input.readlines()
    i=0
#   while i < num_bits:
    while 1:
        for line in lines:
            for word in line:
#               for letter in word:
#                   if ord(letter) == 255:
#                       break
                    buttz = ''
                    #print(encoding[all_chars.index(letter)])
#                   for bit in encoding[all_chars.index(letter)]:
                    for bit in encoding[all_chars.index(word)]:
                        buttz += str(bit)
#                       print(bit)
                        output.writebit(int(bit))
#                   output.writebits(encoding[all_chars.index(letter)],len(encoding[all_chars.index(letter)]))
                    i+=len(buttz)
        print("num_bits: ",i)
        break
        

#f = open(output,'r')
#f.seek(bits_written)
#f.write()

#print("num_bits: ", i)

print("time: ", time.clock() - t0)
