## file_compression

These utilities use basic Huffman encoding and decoding to compress and 
decompress text files.

* _huff.py_ encodes, or compresses, a text file, when run with a command line of 
the following format:
 * $ python huff.py text.txt text.huff
* _puff.py_ decodes, or decompresses, a text file, when run with a command line 
of the following format:
 * $ python puff.py text.huff text.puff
* After running the above commands, _text.txt_ and _text.puff_ ought to be 
identical, i.e. the following command will output nothing, indicating the two
files are identical:
 * $ cmp text.txt text.puff

