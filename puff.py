#!/usr/bin/env python
from sys import *
import bit_io
#import itertools
import time

t0 = time.clock()

if len(argv) != 3:
    stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
    exit(2)

# get encoding key header from file here
# store the encoding as a list of tuples:
# e.g.: [(char1,code1),(char2,code2),...]
# OR store them as a 256 element list, with the index indicating the ASCII code
# e.g.: codes = range(256)
# codes[65] = 0101
# codes[66] = 01011 etc....

output_string = '' # text to be output
alphabet = "".join(chr(x) for x in xrange(256)) # all 256 ASCII characters
#codes = [False for i in xrange(256)] # list to hold all encodings
codes = []
tuples = []
all_chars = [] # all the chars that are being encoded
enc_lens = [] # lengths of encoded chars (entries correspond w/all_chars')
bits_read = 0
bytes_read = 0

with bit_io.BitReader(argv[1]) as input, open(argv[2], 'w') as output:
    code_indices = codes.index
#   while 1:
    # read the at least the minimum number of bits we can expect at a time

    num_chars = input.readbits(8) # (correctly) reads # of chars encoded
    bits_read += 8

    # read in chars that're encoded, and their encoding lengths
    for i in xrange(num_chars):
        # need to convert the string to series of 0s and 1s
        #output.writebits(int(all_chars[i],2),8)
        all_chars.append(input.readbits(8))
        enc_lens.append(input.readbits(7))
        bits_read += 15
    letters = [chr(x) for x in all_chars]
    print("letters: ",letters)
    print("bits_read: ",bits_read)

########### EVERYTHING ABOVE HERE VERIFIED CORRECT ###########

    for i in xrange(len(all_chars)):
        codes.append(bin(input.readbits(enc_lens[i]))[2:].zfill(enc_lens[i]))
        bits_read += (enc_lens[i])
    print("codes: ",codes)
    print("bits_read: ", bits_read)
#   print("codes[letters.index('e')]: ",codes[letters.index('e')])

########### EVERYTHING ABOVE HERE MOST LIKELY CORRECT ###########

    num_bits = input.readbits(64)
    num_bytes = input.readbits(64)
    print("num_bits: ",num_bits)
    print("num_bytes: ",num_bytes)

    curr_string = ''
    bit = 0
    letter_counts = 0
#   while 1: # bit < num_bits:#None:#1:
    while bit < num_bits: #29444217: #num_bits:
#   while letter_counts <= num_bytes:
        curr_string += (str(input.readbit()))
        #print(input.readbit())
#       bit += 1
        #print(len(curr_string))
        #print(type(curr_string))
        #print(curr_string)
        if "None" in curr_string:
            print("none in curr_string")
            break
        elif curr_string in codes:
#           print('curr_string: ',curr_string)
#           print('codes[codes.index(curr_string)]: ',codes[codes.index(curr_string)])
#           print(curr_string == codes[codes.index(curr_string)])
#           if curr_string == codes[codes.index(curr_string)]:
            letter_counts += 1
#           i = code_indices(int(curr_string))
            i = chr(all_chars[code_indices(curr_string)])
            output_string += i # str(i)
            curr_string = ''
            if len(output_string) > 500:
                output.write(output_string)
#               letter_counts += len(output_string)
#               print("output_string: ", output_string)
                output_string = ''
            #print(output_string)
            #bit += len(chr(all_chars[code_indices(curr_string)]))
        bit += 1

    #c = readbits(min_length) 
    #while c not in codes: #encoding[1]
    #    c += readbit()

    # concats the character to the output string
    #output_string += chr(code_indices(c))
    #if not c: break
    print("output_string: ", output_string)
    print("letter_counts: ",letter_counts)    
    output.write(output_string)

    print('time: ',time.clock() - t0)
