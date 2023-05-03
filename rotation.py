'''
Created on Jul 2, 2017

@author: Viktor Simjanoski
'''
class Rotation(object):
    """
    A class representing a rotation, which is encoded in the mapping field,
    which is a python dictionary expressing what vertex gets moved into the
    old position of what other vertex.
    """
    def __init__(self, mapping):
        self._mapping = mapping
        self._assert()
        self._init_degree()
    
    def  _assert(self):
        assert len(set(self._mapping.keys())) == len(self.mapping) 
        assert len(set(self._mapping.values())) == len(self.mapping)
        assert sorted(self.mapping.keys()) == sorted(self.mapping.values())
        
    def _init_degree(self):
        """
        What power gives the identity mapping (that doesn't change the object it is applied to)
        You can think of it as equivalently the 360 degree rotation. So for example, if this Rotation
        object corresponded to a 60-degree rotation, this function would return 6.
        """
        self._degree = 1
        mapping = {k:v for k, v  in self.mapping.items()}
        while not (all(k == v for k, v in mapping.items())):
            mapping = {k:self.mapping[v] for k, v in mapping.items()}
            self._degree += 1
            if self._degree > 1000:
                raise Exception('The degree of this rotation is too high')
            
            
    @property
    def mapping(self):
        return self._mapping
    
    def power(self, n):
        """
        Applying this same rotation n times
        """
        mapping = {k:k for k in self.mapping}
        for _ in range(n):
            mapping = {k:self.mapping[v] for k, v in mapping.items()}
        return Rotation(mapping)
    
    @property
    def degree(self):
        return self._degree
    
    def __getitem__(self, key):
        return self.mapping[key]
     
    def __hash__(self):
        return hash(tuple(sorted(self.mapping.items())))
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
