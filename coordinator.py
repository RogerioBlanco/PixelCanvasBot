# Thankyou a_tree and Saria!

import sys

def main():
    # check arguments
    if len(sys.argv) != 5:
        raise ValueError('You must provide [start_x] [start_y] [template_width] [template_height] as arguments.')

    # coords
    start_x = int(sys.argv[1])
    start_y = int(sys.argv[2])
    # template dimensions
    t_w = int(sys.argv[3])
    t_h = int(sys.argv[4])

    tx_edge = start_x + t_w
    ty_edge = start_y + t_h

    # the template center coordinates must align with a grid of 960px squares
    nearest_x = (start_x - start_x % 960) + 960
    nearest_y = (start_y - start_y % 960) + 960

    dist_x = nearest_x - start_x
    dist_y = nearest_y - start_y

    pad_x = dist_x * 2 - t_w
    pad_y = dist_y * 2 - t_h

    new_t_w = pad_x + t_w
    new_t_h = pad_y + t_h

    if pad_x < 0 or pad_y < 0:
        raise ValueError('This template crosses a grid line, it may have to be split up.')

    # verify
    if (start_x * 2 + new_t_w) // 2 % 960 != 0 or (start_y * 2 + new_t_h) // 2 % 960 != 0:
        raise ValueError('New center calculation failed verification.')
    
    print("add %spx padding to the right for width %spx" % (pad_x, new_t_w))
    print("add %spx padding to the bottom for height %spx" % (pad_y, new_t_h))
    #print()
    #print("new center would be: %s, %s" % ((start_x * 2 + new_t_w) // 2, (start_y * 2 + new_t_h) // 2))

main()