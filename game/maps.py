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
       ######
       # rrr#
       # ####
       #   s#
       ######



""",

"""
     ##########
     #r  ppp s#
     ##########





""",

"""
    #############
    # rrrrrrrrr #
    ###########p#
              #p#
              #p#
    ###########p#
    #s         o#
    #############


""",

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

"""
    ###   # #   ###
    #r#   #r#   #r#
    #r#   #r#   #r#
    #r#   #y#   #r#
    # #   ###   # #

     o     s     o



""",

"""
            ###
             r
            #p#
       ######p#
       #rrrrro#
       #rrrrr##
       #rrrrrr#
       #rrrr#r#
       #rrrrrr#
       #rrrrrs#
       ########


""",

"""
      ##################
      #
      #o#
      #o#
      #o#
      #o#
      #o#
      #o#

       o


""",

]

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
