map1 = """

   ####
   #
   #        o
           o#o
           #s#o
           o#o
            o        #
                     #
                  ####


"""

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
