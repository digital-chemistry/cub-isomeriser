'''
Created on Jul 7, 2017

@author: Viktor Simjanoski
'''
import itertools


def average_distance(points, distance_func):
    """
    Given a set of points and their pairwise distances, it calculates the average distances
    between a pair of points, averaged over all C(num_points, 2) pairs.
    """
    
    for p0, p1 in itertools.combinations(points, 2):  # assert symmetry
        assert abs(distance_func(p0, p1) - distance_func(p1, p0)) < 1e-7, \
         '{} {} {} {}'.format(p0, p1, distance_func(p0, p1), distance_func(p1, p0))
         
    for p0, p1, p2 in itertools.combinations(points, 3):  # assert triangle inequality
        assert distance_func(p0, p1) + distance_func(p1, p2) >= distance_func(p0, p2) 
        assert distance_func(p0, p2) + distance_func(p1, p2) >= distance_func(p0, p1)
        assert distance_func(p0, p1) + distance_func(p0, p2) >= distance_func(
            p1, p2), '{p0}-{p1}={d01}  {p0}-{p2}={d02}  {p1}-{p2}={d12}'.format(
                p0=p0, p1=p1, p2=p2, d01=distance_func(p0, p1), d02=distance_func(p0, p2),
                d12=distance_func(p1, p2))
    
    # actual calculation happens below
    total_dist = 0.0
    all_pairs = list(itertools.combinations(points, 2))
    for p0, p1 in all_pairs:
        total_dist += distance_func(p0, p1)
    if all_pairs:
        return float(total_dist) / len(all_pairs)
    else:
        return 0.0
