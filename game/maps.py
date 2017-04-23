map1 = """

   ####
   #
   #        o
           o#o
          w#s#o
           o#o
            o       w#w
                 wwww#w
                 *####w
                 wwwwww

"""

map2 = """
    wwwwwwwwwwwwww
    w            w
    w   *        w
    w  *  *      w
    w       *    w
    w s   *      w
    w            w
    wwwwwwwwwwwwww


"""

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
