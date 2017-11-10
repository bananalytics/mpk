import networkx as nx

def get_namednodes(this_G):
    nodes_with_names = []
    for nd in this_G.nodes():
        try:
            if this_G.node[nd]['name']:
                nodes_with_names.append( this_G.node[nd] )
#                 db.mpk_stopnodes.insert_one( this_G.node[nd] )
        except:
            False
#     print nodes_with_names
    return nodes_with_names

def get_stop_nodes(relation_stop_name, namednodes):
	#relation_stop_name example: u'M1 Al. Pokoju'
    stop_nodes = []
    #first match term.
    a = relation_stop_name.encode('utf-8').lower().strip()  # we want to convert to lowercase string to maximize match potential.

    for i in range(0, len(namednodes)):
    	#second match term
        b = namednodes[i]['name']
        b = b.encode('utf-8').lower().strip()
        if a == b:
            stop_nodes.append(namednodes[i])

    return stop_nodes

def get_shortestpath(this_G, nodeA, nodeB):
	nodeA = nodeA
	nodeB = nodeB
	path_len = nx.shortest_path_length(this_G, source=nodeA['osmid'], target=nodeB['osmid'], weight='length')
	path = nx.shortest_path(this_G, source=nodeA['osmid'], target=nodeB['osmid'], weight='length')
	return nodeA, nodeB, path_len, path

"""
input
takes two nx_stop_name_ids arrays
returns: stopA_node, stopB_node, shortest_path_length, shortest_path
"""

def get_twostops_shortestpath(this_G, nx_stop1_listofnodes , nx_stop2_listofnodes ):
    nodesA = nx_stop1_listofnodes    
    nodesB = nx_stop2_listofnodes
    
    stopA_node = None
    stopB_node = None
    shortest_path_length = 100000000
    shortest_path = []

    for a in nodesA:
        for b in nodesB:
            try:
            	a, b, this_path_len, this_path = get_shortestpath(this_G, a, b)
            except:
            	print "Error: couldn't get a shortest path between {A} and {B}".format(A=a, B=b)
            
            if this_path_len < shortest_path_length:
                stopA_node = a
                stopB_node = b
                shortest_path_length = this_path_len
                shortest_path = this_path
    
    return stopA_node, stopB_node, shortest_path_length, shortest_path

def path_get_intermediate_namednodes(namednodes, path, StopAName, StopBName):
    ret = []

    # if (StopAName == "Salwator") or (StopBName == "Salwator") or (StopAName == u'Salwator') or (StopBName == u'Salwator'):
    # 	path2 = path_remove_namednode(namednodes, path, StopAName)
    # 	path3 = path2
    # else:
    path2 = path_remove_namednode(namednodes, path, StopAName)
    path3 = path_remove_namednode(namednodes, path2, StopBName)
    newpath = path3
    for node in namednodes:
        for i in range(0,len(newpath)):
            if path[i] == node['osmid']:
                ret.append(node)

    return ret

def path_remove_namednode(namednodes, path, name):
    removethese = get_stop_nodes(name, namednodes)
    for item in path:
        for removethis in removethese:
            if removethis['osmid'] == item:
                path.remove(item)
    return path
    
def build_segmentdefition(G, a, b, c, na, nb, path, length ):
	geojson = mapping.build_LineString(G, path)
	data = { "stop_a": a, "stop_b" : b, "stop_c" : c, "node_a" : na, "node_b" : nb, "path" : path, "geojson" : geojson, "length" : length }
