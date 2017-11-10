import osmnx as ox
import networkx as nx


def buildOSMnx(file):
	G = ox.graph_from_file(file, simplify=False)
	return G

xmlfile = '/Users/Filip/Dropbox/code/QGIS/Data/Tramwaje-krakow/siec.xml'


def cachenetwork(G,gname):
	nx.write_gpickle(G, "{var}.gpickle".format(var=gname))
	return

def getcached(gname):
	G = nx.read_gpickle("{var}.gpickle".format(var=gname))
	return G
