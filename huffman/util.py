import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''

    # tree_stream is file object
    # do not close file
    # bitreader continues where pickle left off

    tree = pickle.load(tree_stream)

    return tree


def decode_byte(tree, bitreader):
    '''Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    '''
    tree_part = tree
    # do EOF error handling
    end_of_file = False
    while not end_of_file:
        try:
            bit = bitreader.readbit()
            if bit == 0:
                tree_part = tree_part.getLeft()
            elif bit == 1:
                tree_part = tree_part.getRight()

            if isinstance(tree_part, huffman.TreeLeaf):
                # tree leaf stores int
                leaf_value = tree_part.getValue()
                tree_part = tree
                return leaf_value

        except EOFError:
            # EOF leaf stores None
            end_of_file = True
            return None


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    # reads pickle part of stream from compressed file object
    tree = read_tree(compressed)

    # use bitreader to decode rest of bits
    # file is already opened in decompress.py
    # read_tree moved the pointer to the part where the bit sequence begins

    # traverse decoder tree using bits in sequence
    # add resulting leaf to decoded_text

    # do EOF error handling
    reader = bitio.BitReader(compressed)
    writer = bitio.BitWriter(uncompressed)
    byte = decode_byte(tree, reader)    # returns -1 if EOF

    while byte is not None:
        # decoded_text += byte
        # decode byte returns value at leaf node as int
        writer.writebits(byte, 8)
        byte = decode_byte(tree, reader)

    writer.flush()
    uncompressed.flush()


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree, tree_stream)


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    # write pickled tree to compressed file
    write_tree(tree, compressed)

    # encode uncompressed data using tree
    table = huffman.make_encoding_table(tree)

    writer = bitio.BitWriter(compressed)
    reader = bitio.BitReader(uncompressed)    # uncompressed starts at 0

    # leaf stores int values (or None for EOF)
    # read bytes (bits in groups of 8)
    end_of_file = False
    while not end_of_file:
        try:
            # supposed to convert bytes to characters before huffman?
            path = table[reader.readbits(8)]

            for dir in path:
                # go through each True/False in tuple
                # write corresponding bits to compressed
                writer.writebit(dir)

            # print path needed to reach byte
            # reader.read_bits(8)

            # what if the number of bits isnt exactly divisible by 8? (assume)
            # table[read_bits(dfg, 8)]?
            # read_bits returns the translated value

        except EOFError:
            # write EOF indicator (None) to file
            end_of_file = True
            path = table[None]

            for dir in path:
                # go through each True/False in tuple and
                # write corresponding bits to compressed
                writer.writebit(dir)

    writer.flush()
