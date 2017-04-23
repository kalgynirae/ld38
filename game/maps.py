"""

   yyyy
   y
   y        o
           oy 
          #ysy 
           oy 
            o       #y#
                 ####y#
                 *yyyy#
                 ######

"""

maps = [
"""
    #############
    # rrrrrrrrr #
    #p#########r#
    # rrrrrrrrr #
    #r#########y#
    # yyyyyyyyy #
    #r###########
    #oyyyyyyyyys#
    #############


""",
]

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
