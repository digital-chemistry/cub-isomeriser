'''
Created on Jul 3, 2017

@author: Viktor Simjanoski
'''
import itertools
from rotation import Rotation

def compose_rotations(rotations):
    """
    rotations is a list of rotations, each one of which is a Rotation object.
    They are composed in the following way: if rotations=[R1, R2, R3], the composed
    rotation is R1(R2(R3))
    """
    
    assert isinstance(rotations, (list, tuple)), rotations
    assert all(isinstance(rot, Rotation) for rot in rotations)
    keys = tuple(sorted(rotations[0].mapping.keys()))
    for rot in rotations:  # all have same elements
        assert keys == tuple(sorted(rot.mapping.keys()))
        
    mapping = {k:k for k in keys}
    for rot in reversed(rotations):
        mapping = {k:rot[v] for k, v in mapping.items()}
    return Rotation(mapping)

def all_rotations_combos(base_rotations):
    """
    Generate all possible different combinations that can be obtained by combining base_rtations.
    base_rotations is a list of Rotation objectss. 
    """
    assert isinstance(base_rotations, (list, tuple))
    all_rotations = set()
    for rotations in itertools.permutations(base_rotations):
        powers = [list(range(rot.degree)) for rot in rotations]
        powers_combos = itertools.product(*powers)
        for powers_combo in powers_combos:
            powered_rotations = [rot.power(p) for rot, p in zip(rotations, powers_combo)]
            all_rotations.add(compose_rotations(powered_rotations))
    return all_rotations
