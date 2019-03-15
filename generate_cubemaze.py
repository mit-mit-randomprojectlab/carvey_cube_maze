"""
generate_cubemaze.py - Script to produce randomised cube maze
"""

from math import *
import os
import random
from PIL import Image, ImageDraw

class Node(object):
	pass

# maze params
mm2pix = (1/25.4)*96 # 96 ppi
n = 8
output_dir = 'mazes'
output_svg_dir = 'mazes'

# addsideedges: adds edges to graph that traverse the sides of the cube (gets ugly)
def addsideedges(side1,side2,nedge):
	samp = random.sample([i for i in xrange(1,n-1)], nedge)
	for s in samp:
		if side1 == 0:
			if side2 == 1:
				ind1 = n*(n-1)+s
				ind2 = n*n*1+s
			elif side2 == 3:
				ind1 = s
				ind2 = n*n*3+n*(n-1)+s
			elif side2 == 4:
				ind1 = n*s
				ind2 = n*n*4+n*(n-s-1)
			elif side2 == 5:
				ind1 = n*s+(n-1)
				ind2 = n*n*5+n*(n-s-1)+(n-1)
		elif side1 == 2:
			if side2 == 3:
				ind1 = n*n*2+n*(n-1)+s
				ind2 = n*n*3+s
			elif side2 == 1:
				ind1 = n*n*2+s
				ind2 = n*n*1+n*(n-1)+s
			elif side2 == 4:
				ind1 = n*n*2+n*s
				ind2 = n*n*4+n*s+(n-1)
			elif side2 == 5:
				ind1 = n*n*2+n*s+(n-1)
				ind2 = n*n*5+n*s
		elif side1 == 1:
			if side2 == 4:
				ind1 = n*n*1+n*s
				ind2 = n*n*4+s
			elif side2 == 5:
				ind1 = n*n*1+n*s+(n-1)
				ind2 = n*n*5+(n-s-1)
		elif side1 == 3:
			if side2 == 4:
				ind1 = n*n*3+n*s
				ind2 = n*n*4+n*(n-1)+(n-s-1)
			elif side2 == 5:
				ind1 = n*n*3+n*s+(n-1)
				ind2 = n*n*5+n*(n-1)+s
		nodes[ind1].neighbours.append(ind2)
		nodes[ind2].neighbours.append(ind1)

# Initialise maze graph (connected cubes)
nodes = []
for side in xrange(6):
	for j in xrange(n):
		for i in xrange(n):
			nodes.append(Node())
			nodes[-1].coords = (i,j,side)
			nodes[-1].neighbours = []
			if i > 0:
				nodes[-1].neighbours.append(j*n+(i-1)+n*n*side)
			if i < (n-1):
				nodes[-1].neighbours.append(j*n+(i+1)+n*n*side)
			if j > 0:
				nodes[-1].neighbours.append((j-1)*n+i+n*n*side)
			if j < (n-1):
				nodes[-1].neighbours.append((j+1)*n+i+n*n*side)
			nodes[-1].paths = []
			nodes[-1].parent = -1
nedge = 2 # number of randomly located connection points between each cube face
addsideedges(0,1,nedge)
addsideedges(0,3,nedge)
addsideedges(0,4,nedge)
addsideedges(0,5,nedge)
addsideedges(2,3,nedge)
addsideedges(2,1,nedge)
addsideedges(2,4,nedge)
addsideedges(2,5,nedge)
addsideedges(1,4,nedge)
addsideedges(1,5,nedge)
addsideedges(3,4,nedge)
addsideedges(3,5,nedge)

# Run recursive back-substitution algorithm to generate maze
#current_node = random.randint(0,n*n-1)
current_node = 0
nodes[current_node].parent = 6*n*n # special label for starting node
while True:
	unvisited_neighbours = [i for i in nodes[current_node].neighbours if nodes[i].parent == -1]
	if len(unvisited_neighbours) == 0:
		if nodes[current_node].parent == 6*n*n:
			break
		else:
			current_node = nodes[current_node].parent
	else:
		new_node = unvisited_neighbours[random.randint(0,len(unvisited_neighbours)-1)]
		nodes[current_node].paths.append(new_node)
		nodes[new_node].parent = current_node
		current_node = new_node

# need to make all paths two-way first
for node in nodes:
	i = node.coords[0]
	j = node.coords[1]
	side = node.coords[2]
	ind = j*n+i+n*n*side
	for path in node.paths:
		if not ind in nodes[path].paths:
			nodes[path].paths.append(ind)

#################
# plot maze out
gres = 20
wallthick = 4
offsets = [(gres*n,0),(gres*n,gres*n),(gres*n,gres*n*2),(gres*n,gres*n*3),(0,gres*n*2),(gres*n*2,gres*n*2)]
img = Image.new('RGB', (gres*n*3, gres*n*4), color = (0,0,0))
draw = ImageDraw.Draw(img)
for node in nodes:
	i = node.coords[0]
	j = node.coords[1]
	side = node.coords[2]
	xy = [gres*i+wallthick,gres*j+wallthick,gres*i+(gres-wallthick),gres*j+(gres-wallthick)]
	xy[0] += offsets[side][0]
	xy[1] += offsets[side][1]
	xy[2] += offsets[side][0]
	xy[3] += offsets[side][1]
	draw.rectangle(xy, fill=(255,255,255))
	for path in node.paths:
		ip = path % n
		sidep = path/(n*n)
		jp = (path-n*n*sidep)/n
		if side == sidep:
			xy = [gres*i+wallthick,gres*j+wallthick,gres*ip+(gres-wallthick),gres*jp+(gres-wallthick)]
			xy[0] += offsets[side][0]
			xy[1] += offsets[side][1]
			xy[2] += offsets[side][0]
			xy[3] += offsets[side][1]
			draw.rectangle(xy, fill=(255,255,255))
#draw.line(path_wall, fill=(255,255,0))
for node in nodes: # draw lines connecting outer edges in image
	i = node.coords[0]
	j = node.coords[1]
	side = node.coords[2]
	for path in node.paths:
		ip = path % n
		sidep = path/(n*n)
		jp = (path-n*n*sidep)/n
		if not side == sidep:
			if (side in [0,1] and sidep in [0,1]) or (side in [1,2] and sidep in [1,2]) or (side in [2,3] and sidep in [2,3]) or (side in [2,4] and sidep in [2,4]) or (side in [2,5] and sidep in [2,5]):
				xy = [gres*i+wallthick,gres*j+wallthick,gres*ip+(gres-wallthick),gres*jp+(gres-wallthick)]
				xy[0] += offsets[side][0]
				xy[1] += offsets[side][1]
				xy[2] += offsets[sidep][0]
				xy[3] += offsets[sidep][1]
				draw.rectangle(xy, fill=(255,255,255))
			else:
				xy = [gres*i+(gres/2),gres*j+(gres/2),gres*ip+(gres/2),gres*jp+(gres/2)]
				xy[0] += offsets[side][0]
				xy[1] += offsets[side][1]
				xy[2] += offsets[sidep][0]
				xy[3] += offsets[sidep][1]
				#draw.line(xy, fill=(255,0,0))
				xy = [gres*i+wallthick,gres*j+wallthick,0,0]
				if j == 0:
					xy[2] = xy[0]+(gres-2*wallthick)
					xy[3] = xy[1]-2*wallthick
				elif j == (n-1):
					xy[2] = xy[0]+(gres-2*wallthick)
					xy[3] = xy[1]+gres
				elif i == 0:
					xy[2] = xy[0]-2*wallthick
					xy[3] = xy[1]+(gres-2*wallthick)
				elif i == (n-1):
					xy[2] = xy[0]+gres
					xy[3] = xy[1]+(gres-2*wallthick)
				xy[0] += offsets[side][0]
				xy[1] += offsets[side][1]
				xy[2] += offsets[side][0]
				xy[3] += offsets[side][1]
				draw.rectangle(xy, fill=(255,255,255))
#for offset in offsets: # draw outlines of each maze side
#	draw.rectangle([offset[0],offset[1],offset[0]+n*gres,offset[1]+n*gres], outline=(0,255,0))

# draw unused corners to white
draw.rectangle([0,0,gres*n,gres*n], fill=(255,255,255))
draw.rectangle([2*gres*n,0,3*gres*n,gres*n], fill=(255,255,255))
draw.rectangle([0,gres*n,gres*n,2*gres*n], fill=(255,255,255))
draw.rectangle([2*gres*n,gres*n,3*gres*n,2*gres*n], fill=(255,255,255))
draw.rectangle([0,3*gres*n,gres*n,4*gres*n], fill=(255,255,255))
draw.rectangle([2*gres*n,3*gres*n,3*gres*n,4*gres*n], fill=(255,255,255))

img.save(os.path.join(output_dir,'cubemazeout.png'))

###################################
# generate output SVGs for carving
channel_width = 6.0
board_depth = 9.0
edge_width = 3.0
edge_buffer = 1.5

# CreateSVG_side: outputs SVG cut file for given maze side
def CreateSVG_side(side, output_svg):
	rectangles_hor = []
	sp = None
	for j in xrange(n): # search for horizontal rectangles
		i = 0
		while i < n:
			ind = j*n+i+n*n*side
			ind2 = ind+1
			side2 = ind2/(n*n)
			# pickup continuous horizontal paths and solo squares
			if (ind2 in nodes[ind].paths and side2 == side) or (len(nodes[ind].paths) == 1 and nodes[ind].paths[0] == ind2 and not side2 == side):
				if sp is None:
					sp = i
			else:
				if not sp is None:
					rectangles_hor.append([j,sp,i])
					sp = None
			i += 1
	rectangles_vert = []
	sp = None
	for i in xrange(n): # search for vertical rectangles
		j = 0
		while j < n:
			ind = j*n+i+n*n*side
			ind2 = ind+n
			side2 = ind2/(n*n)
			if ind2 in nodes[ind].paths and side2 == side:
				if sp is None:
					sp = j
			else:
				if not sp is None:
					rectangles_vert.append([i,sp,j])
					sp = None
			j += 1

	rectangles_edge = []
	for j in xrange(n): # search for horizontal rectangles
		for i in xrange(n):
			ind = j*n+i+n*n*side
			for ind2 in nodes[ind].paths:
				side2 = ind2/(n*n)
				if not (side2 == side):
					rectangles_edge.append([i,j])

	# create SVGs
	if side in [0,2]:
		offset = [edge_buffer+board_depth,edge_buffer+board_depth]
		outline_size = [n*(channel_width+edge_width)+2*edge_buffer+2*board_depth, n*(channel_width+edge_width)+2*edge_buffer+2*board_depth]
	elif side in [1,3]:
		offset = [edge_buffer+board_depth,edge_buffer]
		outline_size = [n*(channel_width+edge_width)+2*edge_buffer+2*board_depth, n*(channel_width+edge_width)+2*edge_buffer]
	else:
		offset = [edge_buffer,edge_buffer]
		outline_size = [n*(channel_width+edge_width)+2*edge_buffer, n*(channel_width+edge_width)+2*edge_buffer]

	f = open(output_svg, "w");
	f.write('<?xml version="1.0" standalone="no"?>\n')
	f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
	f.write('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'%(ceil(outline_size[0]*mm2pix),ceil(outline_size[1]*mm2pix)))
	f.write('\t<title>Cube Maze side %d</title>\n'%(side))
	f.write('\t<desc>Single side of a cube rolling ball maze, to be carved using Carvey CNC.</desc>\n')
	f.write('\t<g fill="#ffffff" stroke="#000000">\n')
	f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(0,0,outline_size[0]*mm2pix,outline_size[1]*mm2pix))
	f.write('\t</g>\n')
	f.write('\t<g fill="#808080" stroke="#808080">\n')
	for row in rectangles_hor:
		x = offset[0]+edge_width/2+row[1]*(channel_width+edge_width)
		y = offset[1]+edge_width/2+row[0]*(channel_width+edge_width)
		w = ((row[2]-row[1])-1)*(channel_width+edge_width) + 2*(channel_width+edge_width/2)
		h = channel_width
		f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
	for row in rectangles_vert:
		x = offset[0]+edge_width/2+row[0]*(channel_width+edge_width)
		y = offset[1]+edge_width/2+row[1]*(channel_width+edge_width)
		w = channel_width
		h = ((row[2]-row[1])-1)*(channel_width+edge_width) + 2*(channel_width+edge_width/2)
		f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
	for row in rectangles_edge:
		i = row[0]
		j = row[1]
		if i == 0:
			if side in [0,1,2,3]:
				x = offset[0]-(board_depth-channel_width)-edge_buffer
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = edge_buffer+edge_width+(board_depth-channel_width)
				h = channel_width
			else:
				x = offset[0]-edge_buffer
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = edge_buffer+edge_width
				h = channel_width
		elif i == (n-1):
			if side in [0,1,2,3]:
				x = offset[0]+edge_width/2+(n-1)*(channel_width+edge_width)+channel_width
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = edge_buffer+edge_width/2+(board_depth-channel_width)
				h = channel_width
			else:
				x = offset[0]+edge_width/2+(n-1)*(channel_width+edge_width)+channel_width
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = edge_buffer+edge_width/2
				h = channel_width
		elif j == 0:
			if side in [0,2]:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = offset[1]-(board_depth-channel_width)-edge_buffer
				w = channel_width
				h = edge_buffer+edge_width+(board_depth-channel_width)
			else:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = offset[1]-edge_buffer
				w = channel_width
				h = edge_buffer+edge_width
		elif j == (n-1):
			if side in [0,2]:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = offset[1]+edge_width/2+(n-1)*(channel_width+edge_width)+channel_width
				w = channel_width
				h = edge_buffer+edge_width/2+(board_depth-channel_width)
			else:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = offset[1]+edge_width/2+(n-1)*(channel_width+edge_width)+channel_width
				w = channel_width
				h = edge_buffer+edge_width/2
		f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
	f.write('\t</g>\n')
	f.write('\t<g fill="#000000" stroke="#000000">\n')
	for row in rectangles_edge:
		i = row[0]
		j = row[1]
		if i == 0:
			if side in [0,1,2,3]:
				x = -3
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = channel_width+3
				h = channel_width
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
			else:
				x = -3
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = 3
				h = channel_width
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
		elif i == (n-1):
			if side in [0,1,2,3]:
				x = outline_size[0]-channel_width
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = channel_width+3
				h = channel_width
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
			else:
				x = outline_size[0]
				y = offset[1]+edge_width/2+j*(channel_width+edge_width)
				w = 3
				h = channel_width
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
		elif j == 0:
			if side in [0,2]:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = -3
				w = channel_width
				h = channel_width+3
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
			else:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = -3
				w = channel_width
				h = 3
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
		elif j == (n-1):
			if side in [0,2]:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = outline_size[1]-channel_width
				w = channel_width
				h = channel_width+3
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
			else:
				x = offset[0]+edge_width/2+i*(channel_width+edge_width)
				y = outline_size[1]
				w = channel_width
				h = 3
				f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f"/>\n'%(x*mm2pix,y*mm2pix,w*mm2pix,h*mm2pix))
	f.write('\t</g>\n')
	f.write('</svg>\n')
	f.close()

# move through maze and draw channels as rectangles along horizontal and vertical directions
for side in xrange(6):
	CreateSVG_side(side, os.path.join(output_svg_dir,'cubemaze_side%d.svg'%(side)))



