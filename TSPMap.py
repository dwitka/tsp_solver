import math
import operator
import matrix
import tspturtle
import time

coors_list = []
coordinate_list = []
d_list = []
dic_list = []
city_count = [0]
node_count = [3]
optimal_value = [0]
linear_list = []


class Node:
    """Node Class"""
    def __init__(self, value, distanceL=0, right=0, distanceR = 0, left=0):
        """(int-->None)
        node constuctor"""
        self.value = value
        self.distanceL = distanceL
        self.distanceR = distanceR
        self.left = left
        self.right = right

      
    def set_right(self, nodeR):
        """(nodeR-->None)
        sets right node to nodeR"""
        self.right = nodeR
        nodeR.left = self


    def set_left(self, nodeL):
        """(nodeL-->None)
        sets left node to nodeL"""        
        self.left = nodeL
        nodeL.right = self


    def __str__(self):
        """(None-->string)
        returns value of node as a string"""        
        return str(self.value)


def list_from_file():
    """(None--> list of tuples)
    Creates a list of tuples containing number of city 
    and x,y coordinates (name, x, y)"""
    file = open("C:\\Users\\00\\AppData\\Local\\Programs\\Python\\Python36-32\\tsp_solver_master\\map_files\\tsp_test100.txt", "r")
    for line in file:
        city_count[0] = city_count[0] + 1
        line = line.split()
        coordinate_list.append((int(line[0]), int(line[1]), int(line[2])))
        coors_list.append((int(line[1]), int(line[2])))
    file.close()
    return coordinate_list


def distance_list(coordinate_list):
    """(list of tuples-->list of lists)
    calculates the distance between all cities and places them
    in a list of lists."""
    for item1 in coordinate_list:
        L2 = []
        d_list.append(L2)
        for item2 in coordinate_list:
            if item1 != item2:
                distance = math.sqrt((item2[1] - item1[1])**2 \
                                     + (item2[2] - item1[2])**2)
                L2.append((item2[0], distance))
    return d_list   


def get_node_points(node):
    """(node-->tuple)
    return coordinates for node"""
    for item in coordinate_list:
        if item[0] == node.value:
            return (item[1], item[2])


def get_city_points(city):
    """(int-->tuple)
    return coordinates for node"""
    for item in coordinate_list:
        if item[0] == city:
            return (item[1], item[2])

       
def sort_L3():
    """(None-->None)
    sorts the items in each distance list by nearest distance"""
    for item in d_list:
        item.sort(key=operator.itemgetter(1))


def dictionary():
    """(None-->list of {city:{cities:distances}})
    Creates a list of dictionaries where each dictionary
    contains a key(city) and a dictionary value which contains
    key(cities) with value(distances) relating to city."""
    for List1 in d_list:
        dic = {}
        dic1 = {}
        dic[d_list.index(List1) + 1] = dic1
        dic1[d_list.index(List1) + 1] = 0
        for tup in List1:
            dic1[tup[0]] = tup[1]
        dic_list.append(dic)


def remove_eq(new_node):
    """(new_node-->None)
    removes a line from the linear_list corresponding to the line
    being erased from the map"""
    for item in linear_list:
        if (item[0] == new_node.left) & (item[1]== new_node.right):
            linear_list.remove(item)


def remove(node):
    """(node-->None)
    Remove cities from d_list lists which have been added to the map"""
    for liste in d_list:
        for item2 in liste:
            if item2[0] == node.value:
                liste.remove(item2)


def nearest(node):       
    """(node-->(int, int, int))
    Finds the nearest city to the Map"""
    count = 0
    distance = 100000
    while count != node_count[0]:
        city = d_list[node.value - 1]
        if city != []:
            if city[0][1] < distance:
                distance = city[0][1]
                new_city = city[0][0]
                closest_city = node.value
        node = node.left
        count = count + 1
    return (closest_city, new_city, distance)


def angle(l,m,n):
    """((int, int, int)-->float)
    calculates the angle of A"""
    q = round(m**2 + n**2 - l**2, 2)
    r = round(2*m*n, 2)
    return math.acos(q/r)


def distance_between_points(item1, item2):
    """((tuple,tuple)-->int)
    returns the distance between two points"""
    return math.sqrt((item2[1] - item1[1])**2 + (item2[0] - item1[0])**2)   


def shield_right(nodeR, new_city, points, angle0=-1):
    """((nodeR, int, tuple)-->node)
    Find the right node of the shield. The shield is
    a subsection of the map which contains the only viable
    nodes for a new city's connection"""
    item1 = get_node_points(nodeR)
    item2 = get_city_points(new_city)

    a = distance_between_points(item1, points)
    b = distance_between_points(points, item2)
    c = distance_between_points(item1, item2)

    if (b == 0) | (check_point_left(nodeR, nodeR.left, new_city) == True):
        return nodeR
    angle1 = angle(a,b,c)

    if (angle1 < angle0) & (check_points(item2, item1, points, get_node_points(nodeR.left)) == False):
        return nodeR.left
    else:
        nodeR = nodeR.right
        same_side = check_points(item1, get_node_points(nodeR.left), points, item2)
        if same_side == True:
            return shield_right(nodeR, new_city, points, angle1)
        else:
            return nodeR.left


def shield_left(nodeL, new_city, points, angle0=-1):
    """((nodeL, int, tuple)-->node)
    Find the left node of the shield. The shield is
    a subsection of the map which contains the only viable
    nodes for a new city's connection"""
    item1 = get_node_points(nodeL)
    item2 = get_city_points(new_city)

    a = distance_between_points(item1, points)
    b = distance_between_points(points, item2)
    c = dic_list[nodeL.value - 1].get(nodeL.value).get(new_city)

    if (b == 0) | (check_point_left(nodeL, nodeL.right, new_city) == True):
        return nodeL
    angle1 = angle(a,b,c)

    if (angle1 < angle0) & (check_points(item2, item1, points, get_node_points(nodeL.right)) == False):
        return nodeL.right
    else:
        nodeL = nodeL.left
        same_side = check_points(item1, get_node_points(nodeL.right), points, item2)
        if same_side == True:
            return shield_left(nodeL, new_city, points, angle1)
        else:
            return nodeL.right


def add_node(nodeL, nodeR, city):
    """(nodeL, nodeR, int)-->new_node
    Adds a new node to TSP map"""
    new_node = Node(city)
    new_node.set_right(nodeR)
    new_node.set_left(nodeL)
    node_count[0] = node_count[0] + 1
    return new_node


def get_distance(node, value):
    """(node-->int)
    returns the distance between city value and node"""
    return dic_list[node.value - 1].get(node.value).get(value)


def get_intersect_points(line1, line2):
    """((list, list)-->tuple)
    returns the intersect points of two lines"""
    intersect_points = matrix.matrix_sol([line1, line2])
    return intersect_points


def is_between(a, b, c):
    """((int,int,int)-->boolean)
    checks whether "a" falls between "b" and "c" """
    a = round(a, 4)
    b = round(b, 4)
    c = round(c, 4)
    if (a < b) & (a > c):
        return True
    if (a > b) & (a < c):
        return True
    return False


def find_node(node, v):
    """((object, int)-->object)
    Retrieves the node in the map that is closest to the
    nearest city"""
    while node.value != v:
        node = node.right
    return node


def connect_right(nodeR, new_city):
    """((nodeR, int)--> tuple)
    returns tuple of connection values"""
    a = dic_list[nodeR.value - 1].get(nodeR.value).get(nodeR.right.value)
    b = dic_list[nodeR.value - 1].get(nodeR.value).get(new_city)
    c = dic_list[nodeR.right.value - 1].get(nodeR.right.value).get(new_city)
    shortest = b + c - a
    return (nodeR, nodeR.right, new_city, shortest)


def connect_left(nodeL, new_city):
    """((nodeL, int)--> tuple)
    returns tuple of connection values"""    
    a = dic_list[nodeL.value - 1].get(nodeL.value).get(nodeL.left.value)
    b = dic_list[nodeL.value - 1].get(nodeL.value).get(new_city)
    c = dic_list[nodeL.left.value - 1].get(nodeL.left.value).get(new_city)
    shortest = b + c - a
    return (nodeL.left, nodeL, new_city, shortest)

    
def connect_distance(nodeL, nodeR, new_city, shortest0=100000, optimal=("a","b","c","d")):
    """((nodeR, nodeL, int)--> (object, object, int, int))
    The two nodes: nodeR and nodeL, represent the shield boundaries.The 
    function moves along the shield and calculates the shortest distance 
    for the new_city to attach itself to the map."""
    if nodeR == nodeL:
        return optimal    
    a = dic_list[nodeR.value - 1].get(nodeR.value).get(nodeR.left.value)
    b = dic_list[nodeR.value - 1].get(nodeR.value).get(new_city)
    c = dic_list[nodeR.left.value - 1].get(nodeR.left.value).get(new_city)
    shortest1 = b + c - a

    if shortest1 < shortest0:
        optimal = (nodeR.left, nodeR, new_city, shortest1)
    return connect_distance(nodeL, nodeR.left, new_city, optimal[3], optimal)


def optimize_right(connect):
    """(tuple of connection values-->tuple of connection values)
    finds the nearest nodes to the right that will not intersect map
    when new connection lines are made"""
    if intersect(connect[0], connect[1], connect[2]) == False:
        return connect
    else:
        connect = connect_right(connect[1], connect[2])
        if intersect(connect[0], connect[1], connect[2]) == True:
            return optimize_right(connect)
        else:
            return connect


def optimize_left(connect):
    """(tuple of connection values-->tuple of connection values)
    finds the nearest nodes to the left that will not intersect map
    when new connection lines are made"""    
    if intersect(connect[0], connect[1], connect[2]) == False:        
        return connect
    else:
        connect = connect_left(connect[0], connect[2])
        if intersect(connect[0], connect[1], connect[2]) == True:
            return optimize_left(connect)
        else:
            return connect


def is_smaller(connect1, connect2):
    """((tuple, tuple)-->tuple)
    returns the tuple containing the smallest connection distance"""
    if connect1[3] < connect2[3]:
        return connect2
    if connect1[3] > connect2[3]:
        return connect1
    else:
        return connect1


def intersect(nodeL, nodeR, city):
    """((nodeL, nodeR, int)-->boolean)
    determines if the node-city lines intersect with any other map lines"""
    PL = get_node_points(nodeL)
    P = get_city_points(city)
    PR = get_node_points(nodeR)

    equation1 = matrix.linear_eq((PL, P))
    equation2 = matrix.linear_eq((PR, P))

    for item in linear_list:
        lineP1 = get_node_points(item[0])
        lineP2 = get_node_points(item[1])
        temp = item[2][:]
        temp[2] = temp[2]*(-1)
        inter_points = get_intersect_points(equation1, temp)
        if inter_points == "parallel":        
            check1 = False
        else:
            x = is_between(inter_points[0], PL[0], P[0])
            y = is_between(inter_points[0], lineP1[0], lineP2[0])
            check1 = x & y
        if check1 == True:
            return True

    for item in linear_list:
        lineP1 = get_node_points(item[0])
        lineP2 = get_node_points(item[1])        
        temp = item[2][:]
        temp[2] = temp[2]*(-1)        
        inter_points = get_intersect_points(equation2, temp)
        if inter_points == "parallel":        
            check2 = False
        else:        
            x = is_between(inter_points[0], PR[0], P[0])
            y = is_between(inter_points[0], lineP1[0], lineP2[0])
            check2 = x & y
        if check2 == True:
            return True        
    return False


def check_point_right(nodeL, nodeR, city):
    """((nodeL, nodeR, int)-->boolean
    Checks nodeR to see if it back tracks which would give a smaller angle."""
    A = get_city_points(city)    
    B = get_node_points(nodeL)
    C = get_node_points(nodeR)    
    slope = _slope(A,B)
    (F,G) = calibrator(A,B,slope)
    sign = math.copysign(1, ((G[0] - F[0])*(C[1] - F[1]) - (G[1] - F[1])*(C[0] - F[0])))

    if slope == "horizontal":
        if sign == 1:
            if A[0] > B[0]:
                return True
            else:
                return False
        else:
            if A[0] < B[0]:
                return True
            else:
                return False    

    if slope == "vertical":
        if sign == 1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False

    if slope == "inclined":
        if sign == 1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False

    if slope == "declined":
        if sign == 1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False  


def check_point_left(nodeL, nodeR, city):
    """((nodeL, nodeR, int)-->boolean
    Checks nodeL to see if it back tracks which would give a smaller angle."""    
    A = get_city_points(city)    
    B = get_node_points(nodeR)
    C = get_node_points(nodeL)    
    slope = _slope(A,B)
    (F,G) = calibrator(A,B,slope)
    sign = math.copysign(1, ((G[0] - F[0])*(C[1] - F[1]) - (G[1] - F[1])*(C[0] - F[0])))

    if slope == "horizontal":
        if sign == -1:
            if A[0] > B[0]:
                return True
            else:
                return False
        else:
            if A[0] < B[0]:
                return True
            else:
                return False    

    if slope == "vertical":
        if sign == -1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False
    
    if slope == "inclined":
        if sign == -1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False

    if slope == "declined":
        if sign == -1:
            if A[1] < B[1]:
                return True
            else:
                return False
        else:
            if A[1] > B[1]:
                return True
            else:
                return False


def check_points(nodeL, nodeR, points, city):
    """((tuple, tuple, tuple, tuple)-->boolean)
    checks to see whether two nodes are on the same side of
    a line or not"""
    A = points
    B = city    
    C = nodeL
    D = nodeR

    d1 = (B[0] - A[0])*(C[1] - A[1]) - (B[1] - A[1])*(C[0] - A[0])
    d2 = (B[0] - A[0])*(D[1] - A[1]) - (B[1] - A[1])*(D[0] - A[0])

    if (d1 < 0) & (d2 < 0):
        return True
    if (d1 > 0) & (d2 > 0):
        return True
    else:
        return False


def nearest_line(city_points):
    """(tuple of points-->tuple of nodes and line, or None)
    finds the nearest map line to city"""
    closest = 10000
    nodes = None
    for item in linear_list:
        line = item[2]
        nearest = abs(line[1]*city_points[0] + line[0]*city_points[1] + line[2])\
            /math.sqrt(line[1]**2 + line[0]**2)
        x = get_x(line, city_points)
        y = get_y(line, city_points)
        x1 = get_node_points(item[0])[0]
        x2 = get_node_points(item[1])[0]
        y1 = get_node_points(item[0])[1]
        y2 = get_node_points(item[1])[1]        

        if ((x<=x1) & (x>=x2)) | ((x>=x1) & (x<=x2)):
            if ((y<=y1) & (y>=y2)) | ((y>=y1) & (y<=y2)):
                if nearest < closest:
                    closest = nearest
                    nodes = (item[0], item[1], item[2])
    return nodes


def get_x(EQ, M):
    """((list, tuple)-->int)
    returns the x value of the perpendicular point"""
    return (EQ[0]*(EQ[0]*M[0] - EQ[1]*M[1]) - EQ[1]*EQ[2])/(EQ[1]**2 + EQ[0]**2)


def get_y(EQ, M):
    """((list, tuple)-->int)
    returns the y value of the perpendicular point"""    
    return (EQ[1]*((-1)*EQ[0]*M[0] + EQ[1]*M[1]) - EQ[0]*EQ[2])/(EQ[1]**2 + EQ[0]**2)


def check_right(nodeL, nodeR, city):
    """((object, object, int)-->tuple of nodes)
    determines which node is the right node for city to set_right too"""
    A = get_node_points(nodeL)
    B = get_node_points(nodeR)
    C = get_city_points(city)
    slope = _slope(A,B)
    (F,G) = calibrator(A,B,slope) 
    sign = math.copysign(1, ((G[0] - F[0])*(C[1] - F[1]) - (G[1] - F[1])*(C[0] - F[0])))

    if slope == "horizontal":
        if sign == -1:
            if A[0] > B[0]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)
        else:
            if A[0] < B[0]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)    

    if slope == "vertical":
        if sign == -1:
            if A[1] < B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)
        else:
            if A[1] > B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)
     
    if slope == "inclined":
        if sign == -1:
            if A[1] < B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)
        else:
            if A[1] > B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)

    if slope == "declined":
        if sign == -1:
            if A[1] < B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)
        else:
            if A[1] > B[1]:
                return (nodeR, nodeL)
            else:
                return (nodeL, nodeR)


def calibrator(A, B, slope):
    """((tuple,tuple, string)-->(tuple,tuple))
    organizes the points A and B into the correct order"""
    if slope == "horizontal":
        if A[0] > B[0]:
            return (B, A)
        else:
            return(A, B)   
    if slope == "vertical":
        if A[1] > B[1]:
            return (A, B)
        else:
            return(B, A)
    if slope == "inclined":
        if A[0] > B[0]:
            return (A, B)
        else:
            return(B, A)
    if slope == "declined":
        if A[1] > B[1]:
            return (A, B)
        else:
            return(B, A)    


def _slope(A,B):
    """((tuple,tuple)-->string)
    returns the state of a slope"""
    if (B[0] - A[0]) == 0:
        return "vertical"
    slope = (B[1] - A[1])/(B[0] - A[0])
    if slope == 0:
        return "horizontal"
    elif slope > 0:
        return "inclined"
    else:
        return "declined"


def sub_run2(node_left, node, city):
    """(node, node, int)-->None
    If connect_distance takes the same nodes take the best value out of 
    optimize_right and optimize left(this is a quick fix). Then check
    if the lines intersect...add new_city to map."""
    [nodeL, nodeR, new_city, distance] = connect_distance(node_left, node, city[1])
    if  [nodeL, nodeR, new_city, distance] ==  ["a","b","c","d"]:
        oR = optimize_right((node, node.right, city[1], 0))
        oL = optimize_left((node_left, node, city[1], 0))
        [nodeL, nodeR, new_city, distance] = is_smaller(oR, oL)                

    if intersect(nodeL, nodeR, new_city) == True:
        oR = optimize_right((nodeL, nodeL.right, city[1], 0))
        oL = optimize_left((nodeR, nodeR.left, city[1], 0))
        [nodeL, nodeR, new_city, distance] = is_smaller(oR, oL)
    else:
        pass
    new_node = add_node(nodeL, nodeR, new_city)
    sub_run1(new_node, distance)


def sub_run1(new_node, distance): 
    """(new_node, int)-->None
    Adds nodes with line equation to linear_list, removes non-functional
    value. Calls tspturtle to add new map lines."""
    optimal_value[0] = optimal_value[0] + distance

    PL = get_node_points(new_node.left)
    P = get_node_points(new_node)
    PR = get_node_points(new_node.right)

    line1 = matrix.linear_eq((PL, P))
    line2 = matrix.linear_eq((PR, P))

    line1[2] = line1[2]*(-1)
    line2[2] = line2[2]*(-1)

    linear_list.append((new_node.left, new_node, line1))
    linear_list.append((new_node, new_node.right, line2))

    remove_eq(new_node)
    tspturtle.tsp_draw(PL, P, PR)

    remove(new_node)

