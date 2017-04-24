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
            #r#
            # #
       ######%#
       #rrrrro#
       #rrrrr##
       #rrrrrr#
       #rrrr#r#
       #rrrrrr#
       #rrrrrs#
       ########

""",

"""
        #####
        #pppp
        #%#%#
        #r#p#
        #o#o#
        #y#r#
      s  o o



""",

"""
           p
        ###r###
       yyy#y#rrr
      r #     # r
        #%#%#%#
      r #o o o# r
        #  s  #
      r ####### r



""",

"""
      ##########r#
      #yyyyyyyy#%#
      #yrrrrrry#p#
      #rryrryrr#p#
      #rryyyyrr#p#
      #yryyyyry#p#
      #yrryyrryso#
      #yyrrrryy###
      #yyyrryyy#
      ##########


""",

]

def parse(map):
    lines = map.splitlines()
    rows = len(lines)
    for row, line in zip(reversed(range(rows)), lines):
        for col, char in enumerate(line):
            yield (col, row), char
