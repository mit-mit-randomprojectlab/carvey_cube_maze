"""
generate_cubemaze_cover.py - Script to produce cut outs for clear acrylic cover for
3D cube maze: simple screw-in version
"""

from math import *
import os

# maze params
mm2pix = (1/25.4)*96 # 96 ppi
n = 8
channel_width = 6.0
board_depth = 9.0
edge_width = 3.0
edge_buffer = 1.5

cover_thick = 2.0

outline_size = n*(channel_width+edge_width)+2*edge_buffer+2*board_depth
ntabs = 5

screw_rad1 = 3.5/2
screw_rad2 = 4.0

output_dir = 'covers'

# Generate SVG files

# Side panels
f = open(os.path.join(output_dir,'maze_cover_screw.svg'), "w");
f.write('<?xml version="1.0" standalone="no"?>\n')
f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
f.write('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'%(ceil(outline_size*mm2pix),ceil(outline_size*mm2pix)))
f.write('\t<title>Cube Maze Clear Cover</title>\n')
f.write('\t<desc>Cut out for clear acrylic cover for 3D rolling ball cube maze.</desc>\n')

f.write('\t<g fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square">\n')
f.write('\t<rect x="%.6f" y="%.6f" width="%.6f" height="%.6f" rx="%.4f" ry="%.4f"/>\n'%(0,0,outline_size*mm2pix,outline_size*mm2pix,cover_thick*mm2pix,cover_thick*mm2pix))
f.write('\t</g>\n')

f.write('\t<g fill="#000000" stroke="#000000">\n')
f.write('\t\t<circle cx="%.6f" cy="%.6f" r="%.6f"/>\n'%((board_depth/2)*mm2pix,(board_depth/2)*mm2pix,screw_rad1*mm2pix))
f.write('\t\t<circle cx="%.6f" cy="%.6f" r="%.6f"/>\n'%((outline_size-(board_depth/2))*mm2pix,(board_depth/2)*mm2pix,screw_rad1*mm2pix))
f.write('\t\t<circle cx="%.6f" cy="%.6f" r="%.6f"/>\n'%((board_depth/2)*mm2pix,(outline_size-(board_depth)/2)*mm2pix,screw_rad1*mm2pix))
f.write('\t\t<circle cx="%.6f" cy="%.6f" r="%.6f"/>\n'%((outline_size-(board_depth/2))*mm2pix,(outline_size-(board_depth/2))*mm2pix,screw_rad1*mm2pix))
f.write('\t</g>\n')

f.write('</svg>\n')
f.close()
