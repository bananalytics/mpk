import interpretnetwork as intnet
import dbactions as dba
import mapping
"""
get start node
input: G, namednodes, relation
output: start node - nx
"""

def get_startnode(G, namednodes, relation):

	s0 = relation[0]
	s1 = relation[1]


#	ASSUMES GEOLOCATED STOPS

	s0nodes = intnet.get_stop_nodes(s0, namednodes)
	s1nodes = intnet.get_stop_nodes(s1, namednodes)

	#find shortest path
	a_node, b_node, path_len, path = intnet.get_twostops_shortestpath(G, s0nodes , s1nodes )


	#save the start node
	start_node = a_node

	return start_node

"""
get next node
input: G, start_node, relation, current_stop_number
output: next_node, path_len_out, path_out
"""
def get_nextnode(G, start_node, namednodes, relation, current_stop):
	
	i = current_stop
	StopAName = relation[i]
	StopBName = ""
	
	#define stop 0
	s0nodes = []
	s0nodes.append(start_node)
	
	#define stop 2
	s2nodes = []
	
#	 print StopBName
	
	#FUTURE Convert this into a recurvsive function.
	if intnet.get_stop_nodes(relation[i+2], namednodes) == []:
		if intnet.get_stop_nodes(relation[i+3], namednodes) == []:
			if intnet.get_stop_nodes(relation[i+4], namednodes) == []:
				return "stop too far to work"
			else:
				StopBName = relation[i+4]
		else:
			StopBName = relation[i+3]
	else:
		StopBName = relation[i+2]
		
	s2nodes = intnet.get_stop_nodes(StopBName, namednodes)
#	 print s2nodes
	
	# get the shortest path.
	a_node, c_node, path_len, path = intnet.get_twostops_shortestpath(G, s0nodes , s2nodes )

	
	a = start_node
	b_possibilities = intnet.path_get_intermediate_namednodes(namednodes, path, StopAName, StopBName)
	#print b_possibilities
	try:
		b = b_possibilities[0] #this is kinda basic. Just get the first that works.
	except:
		print "Error, couldn't get any nodes between {A} and {B}".format(A=relation[i].encode('utf-8'), B=relation[i+2].encode('utf-8'))
	a, next_node, path_len_out, path_out = intnet.get_shortestpath(G, a, b)
		
	return next_node, path_len_out, path_out

"""
tramnet_get_last_node
input: G, secondtolastnode, relation
output: last_node, path_len_out, path_out
"""

def get_lastnode(G, namednodes, secondtolastnode, relation):
	# get the exact start node (in a list of 1 element, because that's how our shortest path algo works)
	s0nodes = []
	s0nodes.append( secondtolastnode )
	
	#make a list of possible n+1 (last) nodes
	s1 = relation[len(relation)-1]
	s1nodes = intnet.get_stop_nodes(s1, namednodes)

	#find shortest path
	a_node, last_node, path_len_out, path_out = intnet.get_twostops_shortestpath(G, s0nodes , s1nodes )

	return last_node, path_len_out, path_out

"""
tramnet_get_last_node
input: G, relation
output: whole_path, whole_path_len, node_list
"""

def get_wholepath(G, namednodes, relation):
#	 global relnodes
#	 relnodes = relationnodes(relation)
	
	whole_path_len = 0
	whole_path = []
	node_list = []

	#start
	start_node = get_startnode(G, namednodes, relation)
	node_list.append(start_node)
	
	#middle
	a_node = start_node #initialize
	
	for i in range(0, len(relation)-2):
		b_node, path_len_out, path_out = get_nextnode(G, a_node, namednodes, relation, i)
		node_list.append(b_node)
		whole_path_len = whole_path_len + path_len_out
		whole_path.extend( path_out )

		# build the stop definition
		data = build_segmentdefition(G, relation[i], relation[i+1], relation[i+2], a_node, b_node, path_out, path_len_out )
		retobj = dba.set_segmentdefiniton(data)
		# print retobj.inserted_id

		#start over with the next node in the list
		a_node = b_node
	#end
	last_node, path_len_out, path_out = get_lastnode(G, namednodes, a_node, relation)
	
	whole_path_len = whole_path_len + path_len_out
	whole_path.extend( path_out )
	node_list.append(last_node)
	
	
	return whole_path, whole_path_len, node_list

def build_segmentdefition(G, a, b, c, na, nb, path, length ):
	geojson = mapping.build_LineString(G, path)
	data = { "stop_a": a, "stop_b" : b, "stop_c" : c, "node_a" : na, "node_b" : nb, "path" : path, "geojson" : geojson, "length" : length }
	return data



