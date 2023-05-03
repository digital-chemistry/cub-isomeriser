'''
Created on Jul 9, 2017

@author: Viktor Simjanoski
Some correctness checks.
'''
import itertools

def assert_rotations_and_distances(rotations, distance_func):
    "Make sure that the distance between 2 points does not change under a rotation"
    for rot in rotations:
        for a, b in itertools.combinations(rot.mapping.keys(), 2):
            a_image = rot[a]
            b_image = rot[b]
            assert abs(distance_func(a, b) - distance_func(a_image, b_image)) < 1e-15
            if len(a) == 2 and len(b) == 2:
                ab = a.lower() + b.lower()
                ba = b.lower() + a.lower()
                if ab in rot.mapping:
                    assert (rot[ab] == a_image.lower() + b_image.lower() or
                            rot[ab] == b_image.lower() + a_image.lower()), \
                    'a={} b={} ab={} rot[ab]={} a_image={} b_image={}'.format(
                        a, b, ab, rot[ab], a_image, b_image)
                elif ba in rot.mapping:
                    assert (rot[ba] == a_image.lower() + b_image.lower() or
                            rot[ba] == b_image.lower() + a_image.lower())
