"""
generate_simplemaze.py - Script to produce randomised simple maze
"""

from math import *
import os
import random
from PIL import Image, ImageDraw

class Node(object):
	pass

# maze params
n = 20
output_dir = 'mazes'

# Initialise maze graph (simple square maze)
nodes = []
for j in xrange(n):
	for i in xrange(n):
		nodes.append(Node())
		nodes[-1].coords = (i,j)
		nodes[-1].neighbours = []
		if i > 0:
			nodes[-1].neighbours.append(j*n+(i-1))
		if i < (n-1):
			nodes[-1].neighbours.append(j*n+(i+1))
		if j > 0:
			nodes[-1].neighbours.append((j-1)*n+i)
		if j < (n-1):
			nodes[-1].neighbours.append((j+1)*n+i)
		nodes[-1].paths = []
		nodes[-1].parent = -1

# Run recursive back-substitution algorithm to generate maze
#current_node = random.randint(0,n*n-1)
current_node = 0
nodes[current_node].parent = n*n # special label for starting node
while True:
	unvisited_neighbours = [i for i in nodes[current_node].neighbours if nodes[i].parent == -1]
	if len(unvisited_neighbours) == 0:
		if nodes[current_node].parent == n*n:
			break
		else:
			current_node = nodes[current_node].parent
	else:
		new_node = unvisited_neighbours[random.randint(0,len(unvisited_neighbours)-1)]
		nodes[current_node].paths.append(new_node)
		nodes[new_node].parent = current_node
		current_node = new_node

# plot maze out
gres = 20
wallthick = 4
img = Image.new('RGB', (gres*n, gres*n), color = (0,0,0))
draw = ImageDraw.Draw(img)
for node in nodes:
	i = node.coords[0]
	j = node.coords[1]
	draw.rectangle([gres*i+wallthick,gres*j+wallthick,gres*i+(gres-wallthick),gres*j+(gres-wallthick)], fill=(255,255,255))
	for path in node.paths:
		ip = path % n
		jp = path/n
		draw.rectangle([gres*i+wallthick,gres*j+wallthick,gres*ip+(gres-wallthick),gres*jp+(gres-wallthick)], fill=(255,255,255))
img.save(os.path.join(output_dir,'mazeout.png'))

