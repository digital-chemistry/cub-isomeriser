import datetime
import os
import sys
import numpy as np
from rotation import Rotation
from compose_rotations import all_rotations_combos
from count_all_colorings import count_all_colorings
from average_distance import average_distance
from assert_rotations_and_distances import assert_rotations_and_distances

_VERTEX_LABELS = {
                'b2c2':1, 'a2c2':2, 'b1c2':3, 'a1c2':4,
                'a2b2':5, 'a1b2':6, 'a1b1':7, 'a2b1':8,
                'a2c1':9, 'b2c1':10, 'a1c1':11, 'b1c1':12}
"""
2(5, 7) 754
2(2, 7) 653
2(7, 9) 653
2(6, 7) 533.1
2(7, 11) 377

[('a1b1', '0'), ('a1b2', '0')]  #  2(6,7)  # 533.1
[('a1b1', '0'), ('a1c1', '0')]  #  2(7,11) # 377
[('a1b1', '0'), ('a2b2', '0')]  #  2(5,7) # 754
[('a1b1', '0'), ('a2c1', '0')]  #  2(7,9) # 653
[('a1b1', '0'), ('a2c2', '0')]  #  2(2,7) # 653
"""

def _assert_vertices(v0, v1):
    assert not (v0 == v1)
    assert v0[0].lower() in ('a', 'b', 'c')
    assert v1[0].lower() in ('a', 'b', 'c')
    assert len(v0) in (2, 4)
    assert len(v1) in (2, 4)
    if len(v0) > 2:
        assert v0[2].lower() in ('a', 'b', 'c')
    if len(v1) > 2:
        assert v1[2].lower() in ('a', 'b', 'c')

def distance_between_two_vertices(v0, v1):
    """
    These are hard-coded distances based on experimental results.
    """
    _assert_vertices(v0, v1)
        
    if len(v0) == 4 and len(v1) == 4:
        assert v0.lower() == v0
        assert v1.lower() == v1
        if v0[0] == v1[0] and v0[2] == v1[2] and (v0[1] == v1[1] or v0[3] == v1[3]):
            return 533.1
        elif (v0[:2] == v1[:2]) or (v0[2:] == v1[:2]) or (
            (v0[:2] == v1[2:])) or (v0[2:] == v1[2:]) :
            assert not (v0[:3] == v1[:3])
            return 377
        elif v0[0] == v1[0] and v0[2] == v1[2]:
            assert not(v0[1] == v1[1] or v0[3] == v1[3]), '{} {}'.format(
                v0, v1)
            return 754
        elif (v0[0] == v1[0] and not (v0[2] == v1[2])) or (
            (v0[2] == v1[2] and not (v0[0] == v1[0]))) or (
             v0[0] == v1[2] and not (v0[2] == v1[0])) or (
             v0[2] == v1[0] and not (v0[0] == v1[0])):
            assert not (v0[:2] == v1[:2])
            assert not (v0[:2] == v1[2:])
            assert not (v0[2:] == v1[:2])
            assert not (v0[2:] == v1[2:])
            return 653 
        
        

def coloring_to_string(coloring):
    # better_labeled_coloring = {_VERTEX_LABELS[k]:v for k, v in coloring._iteritems()}
    zeros = [k for k, v in coloring if v in (0, '0')]
    twos = [vertex for vertex in zeros if len(vertex) == 4]
    assert len(twos) == len(zeros)
    
    twos = sorted([_VERTEX_LABELS[t] for t in twos])
    twos = [str(t) for t in twos]
    twos_str = ','.join(twos)
    twos_str = '2({}) '.format(twos_str) if len(twos_str) > 0 else ''
    return twos_str
    
def construct_keggin_rots():
    """
    Constructs all the relevant rotations.
    """
    rot1 = Rotation({
        'a1b1':'a2b1', 'a2b1':'a2b2', 'a2b2':'a1b2', 'a1b2':'a1b1',
        'a1c1':'b1c1', 'b1c1':'a2c1', 'a2c1':'b2c1', 'b2c1':'a1c1',
         'a1c2':'b1c2', 'b1c2':'a2c2', 'a2c2':'b2c2', 'b2c2':'a1c2'})
    assert len(rot1.mapping) == 12
    assert rot1.degree == 4
    
    rot2 = Rotation({
        'a1c1':'a2c1', 'a2c1':'a2c2', 'a2c2':'a1c2', 'a1c2':'a1c1',
        'a1b1':'b1c1', 'b1c1':'a2b1', 'a2b1':'b1c2', 'b1c2':'a1b1',
         'a1b2':'b2c1', 'b2c1':'a2b2', 'a2b2':'b2c2', 'b2c2':'a1b2'})
    assert len(rot2.mapping) == 12
    assert rot2.degree == 4
    
    rot3 = Rotation({
        'b1c1':'b1c2', 'b1c2':'b2c2', 'b2c2':'b2c1', 'b2c1':'b1c1',
        'a1c1':'a1b1', 'a1b1':'a1c2', 'a1c2':'a1b2', 'a1b2':'a1c1',
         'a2c1':'a2b1', 'a2b1':'a2c2', 'a2c2':'a2b2', 'a2b2':'a2c1'})
    assert len(rot3.mapping) == 12
    assert rot3.degree == 4
    
    return all_rotations_combos([rot1, rot2, rot3])

def keggin_colorings():
    """
    Constructs all the different colorings.
    The colors are encoded as binary digits: 0s and 1s. We create the colorings by iterating
    over the number of zeros, which ranges from 2 to 9 (inclusive).
    """
    FOLDER_NAME = 'out_keggin'
    if os.path.isdir(FOLDER_NAME):
        print (f"The output directory {FOLDER_NAME} alredy exists, you can see it inside this folder.\nPlease rename it"+
                   " or delete it if you want to regenerate the output.\nOtherwise I am not doing anything. Exiting now.")
        return
    os.mkdir(FOLDER_NAME)
    all_rots = construct_keggin_rots()
    assert len(all_rots) == 24
    assert_rotations_and_distances(all_rots, distance_between_two_vertices)
    # number of zeros is number of vertices in a particular color, then ones is the number of the other color
    # you can think of it as blue color=zero red color=one
    for zeros in range(1, 7): 
        sys.stdout.flush()
        ones = 12 - zeros
        unique_colorings, _ = count_all_colorings(all_rots, zeros, ones)
        colorings_with_distances = []
        for coloring in unique_colorings:    
            zero_vertices = [p[0] for p in coloring if p[1] == '0']
            dist = average_distance(zero_vertices, distance_between_two_vertices)
            colorings_with_distances.append((coloring, dist))
        unique_colorings = [(coloring_to_string(cl), dist) for cl, dist in colorings_with_distances]
        unique_colorings = sorted(unique_colorings, key=lambda x: (-x[1], len(x[0]), x[0]))
  
        file_name = 'keggin_{}zeros_{}.txt'.format(zeros, len(unique_colorings))
        with open(f'{FOLDER_NAME}/{file_name}', 'w') as out_file:
                for ix, coloring in enumerate(unique_colorings, 1):
                    out_file.write('{}. {} {}\n'.format(ix, coloring[0], np.round(coloring[1], 2)))
                print (f'Writing {ix} colorings with {zeros} zeros to {file_name}')
        sys.stdout.flush()

    

    
if __name__ == '__main__':
    print ("Started at ", datetime.datetime.now())
    keggin_colorings()
    print ("Finished at ", datetime.datetime.now())
