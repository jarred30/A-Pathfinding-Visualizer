
A* Pathfinding Visualizer


Overview:

This is a pathfinding visualizer created with Python using the A* search algorithm. The purpose of the program is to allow a visualization of how pathfinding works and to allow users to experiment with a pathfinding algorithm via a GUI.

Instructions:
- Press the 'space' key to reset the pathfinding board.
- Use the right mouse button to place a goal.
	- The first time the right mouse button is pressed a yellow node will be added.
	  This represents the start node.
	- The second time the right mouse button is pressed an orange node will be added.
	  This represents the end node.
- Use the left mouse button to add a wall in which the path cannot pass. You can either
  click each node individually or drag the mouse across several nodes.
- Press the 'return' key to find the shortest path after the start and end nodes are placed.
- Press the 'escape' key at any time to close the program.

How to Run:

With all the necessary files, run the following from the 'A* Pathfinding Visualizer' directory:  python path_finding.py

NOTE:  The Pygame and Numpy libraries must be installed to run this program.