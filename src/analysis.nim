import nimpy


proc square(number: int): int {.exportpy.} =
    var number_to_return: int = number * number
    return number_to_return

#proc get_2D_digraph_image(slice: seq[uint8]) tuple[x, y: uint16] {.exportpy.} =
    #return 

