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
    wwwwwwwwwwwww
    w rrrrrrrrr w
    wpwwwwwwwwwrw
    w rrrrrrrrr w
    wrwwwwwwwwwyw
    w yyyyyyyyy w
    wrwwwwwwwwwww
    woyyyyyyyyysw
    wwwwwwwwwwwww


"""

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
