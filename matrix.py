import math

def linear_eq(x):
    """(tuple-->list)
    turns set of coordinates into a 1 dimensional matrix"""
    if x[1][0] != x[0][0]:
        slope = (x[1][1] - x[0][1])/(x[1][0] - x[0][0])
    else:
        return [0, 1, x[0][0]]
    y_intercept = x[0][1] - slope*x[0][0]
    return [1, slope*(-1), y_intercept]


def matrix_sol(matrix):
    """(list of lists-->tuple)
    Turns a matrix of two equations into a tuple of their 
    intersect coordinates"""
    equation1 = matrix[0]
    equation2 = matrix[1]
    
    temp1 = equation1[:]
    temp1 = negate_equation(temp1)
    equation2 = add_equations(equation2, temp1)
    if equation2[1] != 0:
        equation2 = divide_equation(equation2, equation2[1])
    else:
        return "parallel"
    
    temp2 = equation2[:]
    if equation1[1] != 0:
        if math.copysign(1, temp2[1]) == math.copysign(1, equation1[1]):
            temp2 = negate_equation(temp2)
            temp2 = multiply_equation(temp2, equation1[1])
            equation1 = add_equations(temp2, equation1)
        
    return (equation2[2], equation1[2])


def multiply_equation(equation, factor):
    """((list, int)-->list)
    multiplies each number in the list by the factor and returns
    the resultant list"""
    count = 0
    while count < 3:
        equation[count] = equation[count]*(factor)
        count = count + 1
    return equation      


def divide_equation(equation, factor):
    """((list, int)-->list)
    divides each number in the list by the factor and returns
    the resultant list""" 
    count = 0
    while count < 3:
        equation[count] = equation[count]/(factor)
        count = count + 1
    return equation 

 
def add_equations(equation1, equation2):
    """((list, list)-->list)
    adds the corresponding values in both lists and returns
    a new list"""    
    y = equation1[0] + equation2[0]
    x = equation1[1] + equation2[1]
    b = equation1[2] + equation2[2]
    return [y, x, b]


def negate_equation(equation):
    """(list-->list)
    negates each value in the list and returns the new list"""    
    count = 0
    while count < 3:
        equation[count] = equation[count]*(-1)
        count = count + 1
    return equation