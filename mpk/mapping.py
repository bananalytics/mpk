import geojsonio
import geojson
import json

def draw_linestring ( G, pathlist ):
	dump = build_LineString(G, pathlist)
	display( dump)
	return

def draw_multilinestring ( G, pathlist ):
	dump = build_MultiLineString(G, pathlist)
	display( dump)
	return

def build_LineString(  G, listofnodes ):
	coords = []
	for nd in listofnodes:
		x = G.node[nd]['x']
		y = G.node[nd]['y']
		coords.append( (x,y) )
	data = geojson.LineString(coords)
	dump = geojson.dumps(data, sort_keys=True)
	return dump

def build_MultiLineString(G, pathlist):
	lines = []
	for path in pathlist:
		raw = nodes2coords( G, path )
		lines.append(raw)
	data = geojson.MultiLineString(lines)
	dump = geojson.dumps(data, sort_keys=True)
	return dump

# utils
def display( dump ):
	geojsonio.display(dump)
	return

# helper functions, might not be used

def nodes2coords( G, listofnodes ):
	coords = []
	for nd in listofnodes:
		x = G.node[nd]['x']
		y = G.node[nd]['y']
		coords.append( (x,y) )
	return coords






