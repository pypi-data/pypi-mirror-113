from copy import deepcopy
from functools import reduce

class VectorComponent:

    def __init__(self, index, value) -> None:

        """
            An auxiliary class, creates an attribute that is passed as a component of a vector of the Vector class.
        """

        try:
            if not isinstance(index, int) or isinstance(value, bool):
                raise TypeError("Component creation error: the VectorComponent.index attribute must be an int()\n       In: self.index = index\n       index is a %s" % type(index))
            else:
                self.index = index
        except TypeError as err:
            print(err)
            exit()
        try:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError("Component creation error: the VectorComponent.value attribute must be an int() or float()\n       In: self.value = value\n       value is a %s" % type(value))
            else:
                self.value = value
        except TypeError as err:
            print(err)
            exit()

class Vector:

    def __init__(self, *args) -> None:
        self.__vector = dict()
        
        if len(args): self.__initialize(args)

    def __initialize(self, args):
        """
            Initializes the array with the arguments received in the constructor.
        """
        i = 0
        for arg in args:
            i += 1
            if isinstance(arg, list):
                for x in arg:
                    self.add(VectorComponent(i, x))
                    i += 1
            else:   
                self.add(VectorComponent(i, arg))

    def add(self, component) -> None:
        """
            Adds a component to the vector. The parameter must be an instance of VectorComponent()
        """
        try:
            if not isinstance(component, VectorComponent):
                raise TypeError
            else:
                if component.index in self.__vector:
                    return # (componenet already exists)
                self.__vector[component.index] = component.value
        except TypeError:
            pass
    
    def set(self, index, value) -> None:
        """
            Change the value of vector[n] if n exists in vector.indexes
        """
        if index in self.__vector: self.__vector[index] = value

    def vector(self) -> dict:
        """
            Returns the vector, in a dictionary {index: value}
        """
        return deepcopy(self.__vector)
    
    def indexes(self) -> tuple:
        """
            Returns a tuple with all vector indexes
        """
        return tuple(self.__vector.keys())
    
    def values(self) -> tuple:
        """
            Returns a tuple with all vector values
        """
        return tuple(self.__vector.values())
    
    def component(self, index):
        """
            Returns the value corresponding to the index, or None if it does not exist
        """
        return self.__vector[index] if index in self.__vector else None
    
    def restriction(self, vectorPart) -> tuple:
        """
            Returns a vectors values. If vectorPart is a part of vector.indexes then x[vectorPart]
            denotes the restriction of x to vectorPart, that is, the vector whose component
            q is vector[q] for each q in vectorPart
        """
        return tuple(filter(lambda c: c is not None, [self.component(q) for q in vectorPart]))

    def isNull(self) -> bool:
        """
            Checks whether the vector is null. 
            A vector is null if x[n] = 0 for all n in vector.indexes.
        """
        return all(map(lambda n: n == 0, self.numbers()))

    def multiplyByEscalar(self, escalar) -> dict:
        """
            Returns the vector resulting from multiplying each component of a vector by a scalar.
        """
        for k in self.__vector:
            self.__vector[k] *= escalar

    def divideByEscalar(self, escalar) -> dict:
        """    
            Returns the vector resulting from dividing each component of a vector by a scalar.
        """
        for k in self.__vector:
            self.__vector[k] /= escalar
    
    def copy(self):
        """
            Returns a copy, of the vector
        """
        copy = Vector()
        for k, v in self.vector().items():
            copy.add(component=VectorComponent(index=k, number=v))
        return copy
    
    def map(self, function=lambda _ : _):
        """
            Return the vector resulting from applying a function to each component of the object.
        """
        mapped = Vector()
        for k, v in self.vector().items():
            mapped.add(VectorComponent(k, function(v)))
        return mapped

    @staticmethod
    def equalIndexSet(vec_x, vec_y) -> bool:
        """
            Returns true if vec_x and vex_y are defined on the same set of indices, and false otherwise.
        """
        return vec_x.indexes() == vec_y.indexes()

    @staticmethod
    def bigger(vec_x, vec_y) -> bool:
        """
            Returns True if vec_x[n] is greater than vec_y[n] for all n in vec_x.indexes.
            This comparison only makes sense if both vectors are defined on the same set of indices.
        """
        v_x, v_y = vec_x.vector(), vec_y.vector()
        return all(map(lambda k: v_x[k] > v_y[k], vec_x.indexes()))
    
    @staticmethod
    def smaller(vec_x, vec_y) -> bool:
        """
            Returns True if vec_x[n] is less than vec_y[n] for all n in vec_x.indexes.
            This comparison only makes sense if both vectors are defined on the same set of indices.
        """
        v_x, v_y = vec_x.vector(), vec_y.vector()
        return all(map(lambda k: v_x[k] < v_y[k], vec_x.indexes()))

    @staticmethod
    def biggerOrEqual(vec_x, vec_y) -> bool:
        """
            Returns True if vec_x[n] is greater than or equal to vec_y[n] for all n in vec_x.indexes.
            This comparison only makes sense if both vectors are defined on the same set of indices.
        """
        v_x, v_y = vec_x.vector(), vec_y.vector()
        return all(map(lambda k: v_x[k] >= v_y[k], vec_x.indexes()))
    
    @staticmethod
    def smallerOrEqual(vec_x, vec_y) -> bool:
        """
            Returns True if vec_x[n] is less than or equal to vec_y[n] for all n in vec_x.indexes.
            This comparison only makes sense if both vectors are defined on the same set of indices.
        """
        v_x, v_y = vec_x.vector(), vec_y.vector()
        return all(map(lambda k: v_x[k] <= v_y[k], vec_x.indexes()))

    @staticmethod
    def sum(vec_x, vec_y):
        """
            Returns the sum of two vectors in an instance of Vector()
            This operations only makes sense if both vectors are defined on the same set of indices.
        """
        v = Vector()
        v_x, v_y = vec_x.vector(), vec_y.vector()
        for k in vec_x.indexes(): v.add(VectorComponent(k, v_x[k] + v_y[k])) 
        return v

    @staticmethod
    def product(vec_x, vec_y):
        """
            Returns the product given by vec_x[n] * vec_y[n] for all n in vec_x.indexes.
            This operations only makes sense if both vectors are defined on the same set of indices.
        """
        v_x, v_y = vec_x.vector(), vec_y.vector()
        return reduce(lambda v, v_ : v + v_, [v_x[k] * v_y[k] for k in vec_x.indexes()])    
    