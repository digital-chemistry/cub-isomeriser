'''
Created on Jul 3, 2017

@author: Viktor Simjanoski
'''
import sys
import itertools

def count_all_colorings(all_rotations, zeros, ones):
    """
    Counts all distinct colorings subject to all_rotiations, with a specific
    numbers of zeros and ones. Assumes there are 2 colors.
    """
    vertices = sorted(list(all_rotations)[0].mapping.keys())
    assert (rot.mapping.keys() == vertices for rot in all_rotations)
    vertices = sorted(vertices)
    colors = ['0'] * zeros + ['1'] * ones
    assert len(colors) == len(vertices), '{} vs {}'.format(colors, vertices)
    unique_colorings = set()
    all_colorings = set()
    for zero_indices in sorted(list(itertools.combinations(range(len(colors)), zeros))):
        colors_perm=['1']*len(colors)
        for ix in zero_indices:
            colors_perm[ix]='0'
        sys.stdout.flush()
        coloring = {v:c for v, c in zip(vertices, colors_perm)}
        coloring_str = ''.join(vc[1] for vc in sorted(coloring.items(), key=lambda pair: pair[0]))
        if coloring_str not in all_colorings:
            unique_colorings.add(tuple(sorted(coloring.items(), key=lambda pair:pair[0])))
            for rot in all_rotations:
                rotated_coloring = {v:coloring[rot[v]] for v, c in coloring.items()}
                rotated_coloring = ''.join(vc[1] for vc in sorted(rotated_coloring.items(), key=lambda pair: pair[0]))
                all_colorings.add(rotated_coloring)
    return unique_colorings, all_colorings
                 
