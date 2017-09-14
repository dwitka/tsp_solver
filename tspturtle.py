import turtle
f = 16

def draw(L):
    """(list of tuples-->None)
    Draws a line from one set of coordinates to the next
    until all coordinates have been connected and then
    returns to starting points."""
    turtle.speed(10)
    length = L.__len__() - 1
    for item in L:
        turtle.penup()
        turtle.goto(item[0] *f, item[1]*f)
        turtle.pendown()
        x = L.index(item)
        if x  != length:
            turtle.goto(L[x + 1][0]*f, L[x + 1][1]*f)
        else:
            turtle.goto(L[0][0]*f, L[0][1]*f)
    
    
def draw_points(L):
    """(list of tuples-->None)
    Draws a point for every set of coordinates in the list 
    and then calls draw() to connect the points."""    
    turtle.setworldcoordinates(-100,-100,1000,1000)
    for item in L:
        turtle.penup()
        turtle.goto(item[0]*f, item[1]*f)
        turtle.pendown()
        turtle.goto(item[0]*f + 1, item[1]*f)
        turtle.goto(item[0]*f + 1, item[1]*f +1)
        turtle.goto(item[0]*f -1 , item[1]*f +1)
        turtle.goto(item[0]*f -1 , item[1]*f -1)
        turtle.goto(item[0]*f + 2 , item[1]*f - 1)
        turtle.hideturtle()
    #draw(L)  

    
def tsp_draw(PL, P, PR):
    """((tuple, tuple, tuple)-->None)
    graphically connects node P to points on map PL and PR,
    while erasing the line from PL to PR"""
    turtle.penup()
    turtle.goto(PL[0]*f, PL[1]*f)
    turtle.pendown()
    turtle.pencolor("white")
    turtle.goto(PR[0]*f, PR[1]*f)
    turtle.pencolor("black")
    turtle.goto(P[0]*f, P[1]*f)
    turtle.goto(PL[0]*f, PL[1]*f)
        

        
def exit_turtle():
    """(None-->None) 
    closes the turtle on click"""
    turtle.exitonclick()
        
