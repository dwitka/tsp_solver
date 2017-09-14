from TSPMap import *

def setup(): 
    """(None-->Node)
    INITIAL SETUP...sets up first three nodes"""
    d_list = distance_list(coordinate_list)
    sort_L3()
    dictionary()
    
    node1 = Node(1)
    
    node2 = Node(d_list[0][0][0])
    opv = get_distance(node1, node2.value)
    optimal_value[0] = optimal_value[0] + opv
    
    node3 = Node(d_list[0][1][0])
    opv = get_distance(node1, node3.value)
    optimal_value[0] = optimal_value[0] + opv
    
    opv = get_distance(node3, node2.value)
    optimal_value[0] = optimal_value[0] + opv    
    

    A = get_node_points(node1)
    B = get_node_points(node2)    
    C = get_node_points(node3)
    
    nodes = check_right(node1, node2, node3.value)
    node3.set_right(nodes[1])
    node3.set_left(nodes[0])
    
    nodes[1].set_right(nodes[0])
    nodes[0].set_left(nodes[1])    
    
    remove(node1)
    remove(node2)
    remove(node3)
    
    PL = get_node_points(nodes[0])
    P = get_node_points(node3)
    PR = get_node_points(nodes[1])
    
    line1 = matrix.linear_eq((PL, P))
    line2 = matrix.linear_eq((PR, P))
    line3 = matrix.linear_eq((PR, PL))
    
    line1[2] = line1[2]*(-1)
    line2[2] = line2[2]*(-1)
    line3[2] = line3[2]*(-1)
    
    linear_list.append((nodes[1], nodes[0], line3))
    linear_list.append((nodes[0], node3, line1))
    linear_list.append((node3, nodes[1], line2))
    
    L = (PL, P, PR)
    tspturtle.draw(L)    
    
    return node1
   
      
def run(node1):
    """(node-->None)
    RUN TO COMPLETION...finishes TSP map"""
    if node_count[0] == city_count[0]:
        return "exit"
    else:
        city = nearest(node1)
        node = find_node(node1, city[0])
        
        eR = get_distance(node, node.right.value)
        f = get_distance(node, city[1])
        gR = get_distance(node.right, city[1])
        
        eL = get_distance(node, node.left.value)
        gL = get_distance(node.left, city[1])        
          
        scale1 = angle(eR,f,gR)
        scale2 = angle(eL,f,gL)
        
        if (scale1 == 0) & (scale2 == 0):
            if eR > eL:
                distance = f + gL - eL
                new_node = add_node(node, node.right, city[1])
                sub_run1(new_node, distance)  
            else:
                distance = f + gR - eR
                new_node = add_node(node.left, node, city[1])
                sub_run1(new_node, distance)
                
        elif scale1 == 0:
            distance = f + gR - eR
            new_node = add_node(node.left, node, city[1])
            sub_run1(new_node, distance)
            
        elif scale2 == 0:
            distance = f + gL - eL
            new_node = add_node(node, node.right, city[1])
            sub_run1(new_node, distance)
            
        else:
            city_points = get_city_points(city[1])
            nodes = nearest_line(city_points)
            if nodes == None:
                if check_point_right(node, node.right, city[1]) == False:
                    nodeR = node
                else:
                    nodeR = shield_right(node.right, city[1], get_node_points(node))
                
                if check_point_left(node.left, node, city[1]) == False:
                    nodeL = node
                else:                    
                    nodeL = shield_left(node.left, city[1], get_node_points(node))                   
                sub_run2(nodeL, nodeR, city)                       
            else:
                (left, right, EQ) = nodes
                x = get_x(EQ, city_points)
                y = get_y(EQ, city_points) 
                
                if get_distance(node, city[1]) < math.sqrt(((y - city_points[1])**2) + ((x - city_points[0])**2)):
                   
                    nodeR = shield_right(node.right, city[1], get_node_points(node))
                    nodeL = shield_left(node.left, city[1], get_node_points(node))        
                    sub_run2(nodeL, nodeR, city)                      
                    
                else:
                    nodeR = shield_right(right, city[1], (x,y))
                    nodeL = shield_left(left, city[1], (x,y))            
                    sub_run2(nodeL, nodeR, city)                             
    run(node1)
          
if __name__ == '__main__':
    start_time = time.time()
    list_from_file()
    tspturtle.draw_points(coors_list)
    node1 = setup()
    
    run(node1)         
    tspturtle.exit_turtle()
    stop_time = time.time() 
    
    print("{0:.6f}".format(stop_time - start_time))
    print(optimal_value[0])
    count = 0
    
    while count != node_count[0]:
        print(node1)
        node1 = node1.right
        count = count +1
        