"""
If we are presented with the first k terms of a sequence it is impossible to say with
certainty the value of the next term, as there are infinitely many polynomial functions
that can model the sequence.

As an example, let us consider the sequence of cube
numbers. This is defined by the generating function,
u(n) = n3: 1, 8, 27, 64, 125, 216, ...

Suppose we were only given the first two terms of this sequence. Working on the
principle that "simple is best" we should assume a linear relationship and predict the
next term to be 15 (common difference 7). Even if we were presented with the first three
terms, by the same principle of simplicity, a quadratic relationship should be
assumed.

We shall define OP(k, n) to be the nth term of the optimum polynomial
generating function for the first k terms of a sequence. It should be clear that
OP(k, n) will accurately generate the terms of the sequence for n ≤ k, and potentially
the first incorrect term (FIT) will be OP(k, k+1); in which case we shall call it a
bad OP (BOP).

As a basis, if we were only given the first term of sequence, it would be most
sensible to assume constancy; that is, for n ≥ 2, OP(1, n) = u(1).

Hence we obtain the
following OPs for the cubic sequence:

OP(1, n) = 1            1, 1, 1, 1, ...
OP(2, n) = 7n-6         1, 8, 15, ...
OP(3, n) = 6n^2-11n+6   1, 8, 27, 58, ...
OP(4, n) = n^3          1, 8, 27, 64, 125, ...

Clearly no BOPs exist for k ≥ 4.

By considering the sum of FITs generated by the BOPs (indicated in red above), we
obtain 1 + 15 + 58 = 74.

Consider the following tenth degree polynomial generating function:

1 - n + n^2 - n^3 + n^4 - n^5 + n^6 - n^7 + n^8 - n^9 + n^10

Find the sum of FITs for the BOPs.
"""


from typing import Callable, List, Union

Matrix = List[List[Union[float, int]]]


def solve(matrix: Matrix, vector: Matrix) -> Matrix:
    """
    Solve the linear system of equations Ax = b (A = "matrix", b = "vector")
    for x using Gaussian elimination and back substitution. We assume that A
    is an invertible square matrix and that b is a column vector of the
    same height.
    >>> solve([[1, 0], [0, 1]], [[1],[2]])
    [[1.0], [2.0]]
    >>> solve([[2, 1, -1],[-3, -1, 2],[-2, 1, 2]],[[8], [-11],[-3]])
    [[2.0], [3.0], [-1.0]]
    """
    size: int = len(matrix)
    augmented: Matrix = [[0 for _ in range(size + 1)] for _ in range(size)]
    row: int
    row2: int
    col: int
    col2: int
    pivot_row: int
    ratio: float

    for row in range(size):
        for col in range(size):
            augmented[row][col] = matrix[row][col]

        augmented[row][size] = vector[row][0]

    row = 0
    col = 0
    while row < size and col < size:
        # pivoting
        pivot_row = max(
            [(abs(augmented[row2][col]), row2) for row2 in range(col, size)]
        )[1]
        if augmented[pivot_row][col] == 0:
            col += 1
            continue
        else:
            augmented[row], augmented[pivot_row] = augmented[pivot_row], augmented[row]

        for row2 in range(row + 1, size):
            ratio = augmented[row2][col] / augmented[row][col]
            augmented[row2][col] = 0
            for col2 in range(col + 1, size + 1):
                augmented[row2][col2] -= augmented[row][col2] * ratio

        row += 1
        col += 1

    # back substitution
    for col in range(1, size):
        for row in range(col):
            ratio = augmented[row][col] / augmented[col][col]
            for col2 in range(col, size + 1):
                augmented[row][col2] -= augmented[col][col2] * ratio

    # round to get rid of numbers like 2.000000000000004
    return [
        [round(augmented[row][size] / augmented[row][row], 10)] for row in range(size)
    ]


def interpolate(y_list: List[int]) -> Callable[[int], int]:
    """
    Given a list of data points (1,y0),(2,y1), ..., return a function that
    interpolates the data points. We find the coefficients of the interpolating
    polynomial by solving a system of linear equations corresponding to
    x = 1, 2, 3...

    >>> interpolate([1])(3)
    1
    >>> interpolate([1, 8])(3)
    15
    >>> interpolate([1, 8, 27])(4)
    58
    >>> interpolate([1, 8, 27, 64])(6)
    216
    """

    size: int = len(y_list)
    matrix: Matrix = [[0 for _ in range(size)] for _ in range(size)]
    vector: Matrix = [[0] for _ in range(size)]
    coeffs: Matrix
    x_val: int
    y_val: int
    col: int

    for x_val, y_val in enumerate(y_list):
        for col in range(size):
            matrix[x_val][col] = (x_val + 1) ** (size - col - 1)
        vector[x_val][0] = y_val

    coeffs = solve(matrix, vector)

    def interpolated_func(var: int) -> int:
        """
        >>> interpolate([1])(3)
        1
        >>> interpolate([1, 8])(3)
        15
        >>> interpolate([1, 8, 27])(4)
        58
        >>> interpolate([1, 8, 27, 64])(6)
        216
        """
        return sum(
            round(coeffs[x_val][0]) * (var ** (size - x_val - 1))
            for x_val in range(size)
        )

    return interpolated_func


def question_function(variable: int) -> int:
    """
    The generating function u as specified in the question.
    >>> question_function(0)
    1
    >>> question_function(1)
    1
    >>> question_function(5)
    8138021
    >>> question_function(10)
    9090909091
    """
    return (
        1
        - variable
        + variable ** 2
        - variable ** 3
        + variable ** 4
        - variable ** 5
        + variable ** 6
        - variable ** 7
        + variable ** 8
        - variable ** 9
        + variable ** 10
    )


def solution(func: Callable[[int], int] = question_function, order: int = 10) -> int:
    """
    Find the sum of the FITs of the BOPS. For each interpolating polynomial of order
    1, 2, ... , 10, find the first x such that the value of the polynomial at x does
    not equal u(x).
    >>> solution(lambda n: n ** 3, 3)
    74
    """
    data_points: List[int] = [func(x_val) for x_val in range(1, order + 1)]

    polynomials: List[Callable[[int], int]] = [
        interpolate(data_points[:max_coeff]) for max_coeff in range(1, order + 1)
    ]

    ret: int = 0
    poly: int
    x_val: int

    for poly in polynomials:
        x_val = 1
        while func(x_val) == poly(x_val):
            x_val += 1

        ret += poly(x_val)

    return ret


if __name__ == "__main__":
    print(f"{solution() = }")