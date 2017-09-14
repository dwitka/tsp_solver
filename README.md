tsp-solver
==========

Solves a tsp problem and shows the solution graphically by displaying the dots first then by 
connecting them. Each connection is closed so you get to see one path disappear as two new paths
are drawn. A bunch of text files have been included -containing coordinate data- so you can test
different maps out; just change the text file on line 49 of the TSPMap.py module. The program 
itself is visually stunning. I hope you like it.

main.py: runs the program

TSPMap.py: The algorithm focuses on preventing lines from crossing and by focusing on reducing total
            calculations. This is done by using various geometric functions.
            
tspturtle.py: Uses turtle to display the output graphically.

matrix.py: Solves a 2 by 3 matrix.
