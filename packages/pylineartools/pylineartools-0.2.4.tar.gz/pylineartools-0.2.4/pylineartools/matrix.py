from copy import deepcopy
from random import randint, random
from .vector import Vector, VectorComponent

class MatrixComponent:

    def __init__(self, row, col, value) -> None:
        try:
            if not all(isinstance(arg, int) for arg in (row, col)) or any(isinstance(arg, bool) for arg in (row, col)):
                raise TypeError("The row and col attributes must be of type int()")
            else:
                self.row = row
                self.col = col
        except TypeError as err:
            print(err)
            exit()
        try:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError("The value attribute must be of type int() or float()")
            else:
                self.value = value
        except TypeError as err:
            print(err)
            exit()

class Matrix:

    def __init__(self, rows=0, cols=0) -> None:
        self.__rows = list()
        self.__cols = list()
        self.__matrix = dict()

        if all(isinstance(arg, int) for arg in (rows, cols)):
            if rows or cols: self.__initialize(rows=rows, cols=cols)

    def __initialize(self, rows, cols) -> None:
        """
                Constructive method, which creates a matrix with the dimensions received.
        """
        for row in range(1, rows + 1):
            if not row in self.__matrix: self.__matrix[row] = dict()
            for col in range(1, cols + 1):
                self.__matrix[row][col] = None
                self.__updateRowColList(row, col)

    def __updateRowColList(self, row, col) -> None:
        """
            Add the row and column to their respective lists if they do not already contain them.
        """
        if not row in self.__rows: self.__rows.append(row)
        if not col in self.__cols: self.__cols.append(col)

    def __fill(self) -> None:
        """
            When a new column is added this method is called. 
            Its function is to fill the other columns with the 
            new component added (and with the number = None)
        """
        for row in self.__rows:
            for col in self.__cols:
                if not col in self.__matrix[row]:
                    self.__matrix[row][col] = None

    @classmethod
    def __genericIteration(cls, mat_x, mat_y, operation):
        """
            Performs a generic iteration over two matrices of the same dimensions and produces 
            a matrix resulting from the operation passed as argument.
        """
        def makeOperation(r, c):
            if operation == "+": return mat_x.component(r,c) + mat_y.component(r,c)
            if operation == "-": return mat_x.component(r,c) - mat_y.component(r,c)
            if operation == "*": return mat_x.component(r,c) * mat_y.component(r,c)
        
        result = Matrix()
        for r, c in map(lambda i: (i['row'], i['col']), mat_x.indexes()):
            result.add(MatrixComponent(r, c, makeOperation(r,c)))
        return result

    def add(self, component) -> None:
        """
            Adds a component to the array. The parameter must be an instance of MatrixComponent().
            If the component already exists the method will do nothing.
            To modify a value in the array use the change() method.
        """
        try:
            if not isinstance(component, MatrixComponent):
                raise TypeError
            else:
                if component.row in self.__matrix:
                    if component.col in self.__matrix[component.row]:
                        if self.__matrix[component.row][component.col] is not None:
                            return # throw error? (component already exists)
                else:
                    self.__matrix[component.row] = dict()
                
                self.__updateRowColList(row=component.row, col=component.col)
                self.__matrix[component.row][component.col] = component.value
                self.__fill()

        except TypeError:
            pass
    
    def set(self, row, col, value) -> None:
        """
            Change the value of matrix[row][col] if row and col 
            are part of the set of row indices and column indices, respectively.
        """
        if row in self.__matrix:
            if col in self.__matrix[row]:
                self.__matrix[row][col] = value

    def randomize(self, integer=False) -> None:
        """
            Populate the array with pseudorandom values.
            By default the values ​​are floating points [0:1], alternatively they can be set to be integers [1:100]
        """
        for i in self.indexes(): 
            self.__matrix[i['row']][i['col']] = randint(0, 100) if integer else random()

    def matrix(self) -> dict:
        """
            Returns the matrix in a dict {row: {col: number}}
        """
        return deepcopy(self.__matrix)

    def indexes(self) -> list:
        """
            Returns array indices in dicts {row: row, col: col} for all component.
        """
        indexes = list()
        for rowKey in self.__matrix:
            for colKey in self.__matrix[rowKey]:
                indexes.append({'row':rowKey,'col':colKey})
        return indexes

    def values(self):
        """
            Returns a list of values ​​only from the array defined on rowPart and colPart.
            When you want the part to be the whole, rowPart or colPart must be ","
        """
        return [[self.__matrix[row][col] for col in self.__cols] for row in self.__rows]

    def getRow(self, row) -> list:
        """
            Returns the corresponding row of the matrix.
        """
        return [self.__matrix[row][k] for k in self.__matrix[row]]

    def getCol(self, col) -> list:
        """
            Returns the corresponding column of the matrix.
        """
        return [self.__matrix[k][col] for k in self.__matrix]

    def component(self, row, col):
        """
            Returns the matrix[row][col] number if row and col 
            are part of the set of row indices and column indices, respectively.
        """
        if row in self.__matrix:
            if col in self.__matrix[row]:
                return self.__matrix[row][col]
        return None

    def dimensions(self) -> dict:
        """
            Returns the dimensions of the matrix, that is, the number of rows and the number of columns. 
        """
        return {'rows':len(self.__rows),'cols':len(self.__cols)}

    def isNull(self) -> bool:
        """
            Indicates whether the array is null. 
            A matrix M defined over NxM is null if M[n][m] is 0 for all n, m belonging to N and M, respectively.
        """
        for row in self.__rows:
            for col in self.__cols:
                if self.__matrix[row][col] != 0 and self.__matrix[row][col] != None: return False
        return True

    def copy(self):
        """
            Returns a matrix's copy.
        """
        copy = Matrix()
        for i in self.indexes():
            copy.add(MatrixComponent(i['row'], i['col'], self.component(i['row'], i['col'])))
        return copy

    def map(self, function=lambda _ : _):
        """
            Return the matrix resulting from applying a function to each component of the object.
        """
        mapped = Matrix()
        for r, c in map(lambda i: (i['row'], i['col']), self.indexes()):
            mapped.add(MatrixComponent(r, c, function(self.component(r, c))))

        return mapped

    def identity(self):
        """
            Returns the identity matrix of the matrix, if it is a square matrix.
        """
        if len(self.__rows) == len(self.__cols):
            identity = Matrix()
            for r, c in map(lambda i: (i['row'], i['col']), self.indexes()):
                if r == c:
                    identity.add(MatrixComponent(r, c, 1))
                else:
                    identity.add(MatrixComponent(r, c, 0))
            return identity

    def transpose(self):
        """
            Returns a matrix transposition.
        """
        transposed = self.copy()
        for r, c in map(lambda i: (i['row'], i['col']), self.indexes()):
            transposed.set(r, c, self.__matrix[r][c])
        return transposed

    def restriction(self, rowPart, colPart):
        """
            Returns an array defined over all p and q in rowPart and colPart, respectively.
            When you want the part to be the whole, rowPart or colPart must be ","
        """
        if rowPart == ",": rowPart = self.__rows[:]
        if colPart == ",": colPart = self.__cols[:]
        restriction = Matrix()
        for row in rowPart:
            for col in colPart:
                restriction.add(MatrixComponent(row, col, self.__matrix[row][col]))
        return restriction
    
    def multiplyByEscalar(self, escalar) -> None:
        """
            Multiplies each component of the matrix by a scalar.
        """
        for row in self.__rows:
            for col in self.__cols:
                self.__matrix[row][col] *= escalar
    
    def divideByEscalar(self, escalar) -> None:
        """
            Divides each component of the matrix by a scalar.
        """
        for row in self.__rows:
            for col in self.__cols:
                self.__matrix[row][col] /= escalar

    def toVector(self):
        """
            Return a Vector() object with all the components of the array, in the order they were added.
        """
        v, i_ = Vector(), 1
        for r, c in map(lambda i: (i['row'], i['col']), self.indexes()):
            v.add(VectorComponent(i_, self.component(r, c)))
            i_ += 1
        return v

    @staticmethod
    def toMatrix(vector):
        """
            Returns a Matrix( len(vector), 1) with the vector's components.
        """
        if not isinstance(vector, Vector):
            raise TypeError("The Vector must be an instance of Vector().")
        else:
            m = Matrix(len(vector.values()), 1)
            for i, v in zip(vector.indexes(), vector.values()):
                m.set(i, 1, v)
            return m

    @staticmethod
    def sum(mat_x, mat_y):
        """
            Returns the sum of two matrices.
        """
        if mat_x.dimensions() == mat_y.dimensions():
            sum = Matrix.__genericIteration(mat_x, mat_y, operation="+")
            return sum
        else:
            raise IndexError("the matrices must have the same dimensions to calculate the sum")

    @staticmethod
    def subtr(mat_x, mat_y):
        """
            Returns the subtraction of two matrices.
        """
        if mat_x.dimensions() == mat_y.dimensions():
            subtr = Matrix.__genericIteration(mat_x, mat_y, operation="-")
            return subtr
        else:
            raise IndexError("the matrices must have the same dimensions to calculate the subtraction")
    
    @staticmethod
    def hadamard(mat_x, mat_y):
        """
            Returns the hadamard product of two matrices or none . 
            In mathematics, Hadamard's product is a binary operation that 
            takes two matrices of the same dimensions and produces another matrix 
            of the same dimension of the operands, 
            where each element i, j is the product of the elements i, j of the two original matrices.
        """
        if mat_x.dimensions() == mat_y.dimensions():
            hadamard = Matrix.__genericIteration(mat_x, mat_y, operation="*")
            return hadamard
        else:
            raise IndexError("the matrices must have the same dimensions to calculate the Hadamard Product")

    @staticmethod
    def product(mat_x, mat_y):
        """
            Calculates the product of a matrix defined over L x M by a matrix defined over M x N.
            The product is a matrix defined over L x N.
        """ 
        product = Matrix()
        rows = set(map(lambda i: i['row'], mat_x.indexes()))
        cols = set(map(lambda i: i['col'], mat_y.indexes()))
        for i in rows:
            for j in cols:
                mult = [a * b for a, b in zip(mat_x.getRow(i), mat_y.getCol(j))]
                product.add(MatrixComponent(i, j, sum(mult)))
        
        return product